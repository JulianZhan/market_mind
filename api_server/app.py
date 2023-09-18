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
        target_date = request.args.get("date")
        try:
            validate_date(target_date)
        except ValueError as e:
            return jsonify({"message": "invalid date, please use YYYY-MM-DD format"})
        news_sentiment = get_news_sentiment(target_date)
        return jsonify({"message": "success", "data": news_sentiment})


class MarketEmotion(Resource):
    def get(self):
        target_date = request.args.get("date")
        try:
            validate_date(target_date)
        except ValueError as e:
            return jsonify({"message": "invalid date, please use YYYY-MM-DD format"})
        reddit_emotion = get_reddit_emotion(target_date)
        return jsonify({"message": "success", "data": reddit_emotion})


def kafka_consumer():
    """
    consume messages from kafka and emit to socketio
    """
    consumer = Consumer(
        {
            "bootstrap.servers": f"{Config.KAFAK_SERVER}:{Config.KAFKA_PORT}",
            "group.id": "market_trades_streaming_serving",
            "auto.offset.reset": "earliest",
        }
    )
    consumer.subscribe([Config.KAFKA_TOPIC_NAME])
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logger.error(f"Consumer error: {msg.error()}")
            continue
        else:
            decoded_message = decode_avro_message(msg.value(), avro_schema)
            socketio.emit("market_trades", decoded_message)


@socketio.on("connect")
def handle_connect():
    socketio.start_background_task(kafka_consumer)


api.add_resource(MarketSentiment, "/market_sentiment")
api.add_resource(MarketEmotion, "/market_emotion")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, allow_unsafe_werkzeug=True, debug=True)
