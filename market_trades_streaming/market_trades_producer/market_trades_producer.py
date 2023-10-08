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
from typing import Optional, List, Union
from prometheus_client import start_http_server, Counter, Gauge

# Metrics definition
messages_produced: Counter = Counter(
    "python_producer_produced_messages_total", "Total Produced Messages"
)
produce_failures: Counter = Counter(
    "python_producer__failures_total", "Total Produce Failures"
)
connection_errors: Counter = Counter(
    "python_producer_connection_errors_total", "Total Connection Errors"
)
current_retries: Gauge = Gauge("python_producer_current_retries", "Current Retries")


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger: logging.Logger = logging.getLogger(__name__)


# Global Variables
max_retries: int = 5
retry_counter: int = 0
retry_interval: int = 20


finnhub_client: finnhub.Client = finnhub.Client(api_key=Config.FINNHUB_API_KEY)
producer: Producer = Producer(
    {"bootstrap.servers": f"{Config.KAFAK_SERVER}:{Config.KAFKA_PORT}"}
)
avro_schema: Union[avro.schema.Schema, avro.schema.RecordSchema] = avro.schema.parse(
    open("trades_schema.avsc").read()
)
tickers: List[str] = ["BINANCE:BTCUSDT"]
batch_size: int = 1000  # flush after every 1000 messages
message_counter: int = 0


def reset_retry_counter() -> None:
    """
    reset global variables retry_counter and current_retries metircs every 3 hours
    """
    global retry_counter
    while True:
        time.sleep(18000)  # sleep for 3 hour
        retry_counter: int = 0
        current_retries.set(0)
        logger.info(f"Resetting retry_counter. retry_counter: {retry_counter}")


def on_message(ws: websocket.WebSocketApp, raw_msg: str) -> None:
    """
    produce message to kafka when message is received from websocket connection

    Args:
        ws (websocket): websocket connection
        message (str): message received from websocket connection
    """
    global message_counter
    message: dict = json.loads(raw_msg)
    if "data" in message:
        avro_message = avro_encode(
            {"data": message["data"], "type": message["type"]}, avro_schema
        )
        try:
            producer.produce(topic=Config.KAFKA_TOPIC_NAME, value=avro_message)
            messages_produced.inc()
            message_counter += 1
            if message_counter >= batch_size:
                # flush producer after every batch_size messages, kafka will wait for all messages to be sent before next batch
                producer.flush()
                message_counter: int = 0
        except Exception as e:
            logger.error(f"Failed to send message to kafka: {e}, message: {message}")
            produce_failures.inc()
    elif message["type"] == "ping":
        logger.info("Ping received")
    else:
        logger.warning(f"Unknown message received: {message}")


def on_error(ws: websocket.WebSocketApp, error: str) -> None:
    """
    Actions to take when websocket connection encounters an error
    It will retry to connect to websocket connection if max_retries is not reached

    Args:
        ws (websocket.WebSocketApp): _description_
        error (str): _description_
    """
    logger.error(f"### error ###: {error}")
    global retry_counter
    if retry_counter < max_retries:
        retry_counter += 1
        connection_errors.inc()
        current_retries.inc()
        ws.close()
        logger.info(f"Retrying in {retry_interval} seconds")
        time.sleep(retry_interval)
        ws.run_forever()
    else:
        logger.error("Max retries reached, exiting...")
        ws.close()


def on_close(
    ws: websocket.WebSocketApp,
    close_status_code: Optional[int],
    close_msg: Optional[str],
) -> None:
    """
    Actions to take when websocket connection is closed
    It will flush producer before closing websocket connection

    Args:
        ws (websocket.WebSocketApp): _description_
        close_status_code (Optional[int]): _description_
        close_msg (Optional[str]): _description_
    """
    logger.info("### closing websocket ###")
    producer.flush(timeout=5)
    logger.info("### closed ###")


def on_open(ws: websocket.WebSocketApp):
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
    start_http_server(5051)
    reset_thread: threading.Thread = threading.Thread(
        target=reset_retry_counter, daemon=True
    )
    reset_thread.start()

    # open websocket connection
    websocket.enableTrace(True)
    ws: websocket.WebSocketApp = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={Config.FINNHUB_API_KEY}",
        on_message=on_message,
        on_close=on_close,
    )
    # define on_open method after ws is created, so that ws is available in on_open method
    ws.on_open = on_open
    ws.on_error = on_error
    ws.run_forever()
