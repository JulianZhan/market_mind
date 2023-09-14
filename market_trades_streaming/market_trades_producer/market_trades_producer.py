import finnhub
import json
import websocket
import avro.schema
import avro.io
from confluent_kafka import Producer
from utils import ticker_validator, avro_encode
import sys

sys.path.append("../")
from config import Config

# Global Variables
finnhub_client = finnhub.Client(api_key=Config.FINNHUB_API_KEY)
producer = Producer({"bootstrap.servers": f"{Config.KAFAK_SERVER}:{Config.KAFKA_PORT}"})
avro_schema = avro.schema.parse(open("trades_schema.avsc").read())
tickers = ["SPY", "BINANCE:BTCUSDT"]
batch_size = 1000  # flush after every 1000 messages
message_counter = 0


def on_message(ws, message):
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
                producer.flush()
                message_counter = 0
        except Exception as e:
            print(f"Failed to send message to Kafka: {e}")
    else:
        print(f"Market may be closed, message: {message}")


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closing ###")
    producer.flush(timeout=5)
    print("### closed ###")


def on_open(ws):
    for ticker in tickers:
        if ticker_validator(finnhub_client, ticker) == True:
            # subscribe to ticker, if ticker exists
            ws.send(f'{{"type":"subscribe","symbol":"{ticker}"}}')
            print(f"Subscription for {ticker} succeeded")
        else:
            print(f"Subscription for {ticker} failed - ticker not found")


def main():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={Config.FINNHUB_API_KEY}",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    # define on_open method after ws is created, so that ws is available in on_open method
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    main()
