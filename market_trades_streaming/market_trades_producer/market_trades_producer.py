import finnhub
import json
import websocket
import avro.schema
import avro.io
from confluent_kafka import Producer
from utils import ticker_validator, avro_encode
import logging
from config import Config
import time
import threading


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# Global Variables
max_retries = 5
retry_counter = 0
retry_interval = 10


finnhub_client = finnhub.Client(api_key=Config.FINNHUB_API_KEY)
producer = Producer({"bootstrap.servers": f"{Config.KAFAK_SERVER}:{Config.KAFKA_PORT}"})
avro_schema = avro.schema.parse(open("trades_schema.avsc").read())
tickers = ["SPY", "BINANCE:BTCUSDT"]
batch_size = 1000  # flush after every 1000 messages
message_counter = 0


def reset_retry_counter():
    global retry_counter
    while True:
        time.sleep(72000)  # sleep for 20 hour
        retry_counter = 0
        logger.info(f"Resetting retry_counter. retry_counter: {retry_counter}")


def on_message(ws, message):
    """
    produce message to kafka when message is received from websocket connection

    Args:
        ws (websocket): websocket connection
        message (str): message received from websocket connection
    """
    global message_counter
    message = json.loads(message)
    if "data" in message:
        avro_message = avro_encode(
            {"data": message["data"], "type": message["type"]}, avro_schema
        )
        try:
            producer.produce(topic=Config.KAFKA_TOPIC_NAME, value=avro_message)
            message_counter += 1
            if message_counter >= batch_size:
                # flush producer after every batch_size messages, kafka will wait for all messages to be sent before next batch
                producer.flush()
                message_counter = 0
        except Exception as e:
            logger.error(f"Failed to send message to kafka: {e}, message: {message}")

    else:
        logger.warning(f"Market may be closed: {message}")


def on_error(ws, error):
    logger.error(f"### error ###: {error}")
    global retry_counter
    if retry_counter < max_retries:
        retry_counter += 1
        ws.close()
        logger.info(f"Retrying in {retry_interval} seconds")
        time.sleep(retry_interval)
        ws.run_forever()
    else:
        logger.error("Max retries reached, exiting...")
        ws.close()


def on_close(ws, close_status_code, close_msg):
    logger.info("### closing websocket ###")
    producer.flush(timeout=5)
    logger.info("### closed ###")


def on_open(ws):
    """
    when websocket connection is opened, check if tickers exist and subscribe to them

    Args:
        ws (websocket): websocket connection
    """
    for ticker in tickers:
        if ticker_validator(finnhub_client, ticker) == True:
            # subscribe to ticker, if ticker exists
            ws.send(f'{{"type":"subscribe","symbol":"{ticker}"}}')
            logger.info(f"Subscribed to {ticker} successfully")
        else:
            logger.warning(f"Susbscription to {ticker} failed, ticker does not exist")


if __name__ == "__main__":
    reset_thread = threading.Thread(target=reset_retry_counter, daemon=True)
    reset_thread.start()

    # open websocket connection
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={Config.FINNHUB_API_KEY}",
        on_message=on_message,
        on_close=on_close,
    )
    # define on_open method after ws is created, so that ws is available in on_open method
    ws.on_open = on_open
    ws.on_error = on_error
    ws.run_forever()
