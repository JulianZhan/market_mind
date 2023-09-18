from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_socketio import SocketIO
from confluent_kafka import Consumer
from api_utils import (
    get_news_sentiment,
    get_reddit_emotion,
    validate_date,
    decode_avro_message,
    avro_schema,
)
from config import Config
import logging

# set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app)


class MarketSentiment(Resource):
    def get(self):
        try:
            target_date = request.args.get("date")
            validate_date(target_date)
        except ValueError as e:
            return jsonify({"message": "invalid date, please use YYYY-MM-DD format"})

        try:
            news_sentiment = get_news_sentiment(target_date)
            return jsonify({"message": "success", "data": news_sentiment})
        except Exception as e:
            logger.error(f"Error getting news sentiment: {e}")
            return jsonify({"message": "error", "data": {}})


class MarketEmotion(Resource):
    def get(self):
        try:
            target_date = request.args.get("date")
            validate_date(target_date)
        except ValueError as e:
            return jsonify({"message": "invalid date, please use YYYY-MM-DD format"})
        try:
            reddit_emotion = get_reddit_emotion(target_date)
            return jsonify({"message": "success", "data": reddit_emotion})
        except Exception as e:
            logger.error(f"Error getting reddit emotion: {e}")
            return jsonify({"message": "error", "data": {}})


def kafka_consumer():
    """
    continuously listen to the kafka topic and emit the message to the socketio client
    """

    # set up kafka consumer
    consumer = Consumer(
        {
            "bootstrap.servers": f"{Config.KAFAK_SERVER}:{Config.KAFKA_PORT}",
            "group.id": "market_trades_streaming_serving",
            "auto.offset.reset": "latest",
        }
    )
    consumer.subscribe([Config.KAFKA_TOPIC_NAME])
    while True:
        # consumer will fetch the message received in the last 1 second from the kafka topic
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logger.error(f"Consumer error: {msg.error()}")
            continue
        else:
            # decode the avro message from kafka topic
            decoded_message = decode_avro_message(msg.value(), avro_schema)
            # emit the message to the socketio client
            socketio.emit("market_trades", decoded_message)


@socketio.on("connect")
def handle_connect():
    # start a background thread to listen to the kafka topic
    socketio.start_background_task(kafka_consumer)
    logger.info("socketio client connected")


api.add_resource(MarketSentiment, "/market_sentiment")
api.add_resource(MarketEmotion, "/market_emotion")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, allow_unsafe_werkzeug=True, debug=True)
