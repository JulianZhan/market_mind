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
from prometheus_client import (
    Counter,
    Gauge,
    make_wsgi_app,
    Histogram,
)
import time


# set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# set up flask app, api and socketio
app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app)


# metrics definition for prometheus monitoring
restful_api_request_latency = Histogram(
    "restful_api_request_latency_seconds",
    "Flask Request Latency",
    ["method", "endpoint"],
)
restful_api_request_count = Counter(
    "restful_api_request_count",
    "Flask Request Count",
    ["method", "endpoint", "http_status"],
)
socket_io_active_connections = Gauge(
    "socket_io_active_connections", "Number of active socketio connections"
)
socket_io_messages_received = Counter(
    "socket_io_messages_received", "Number of messages received by socketio"
)
socket_io_messages_published = Counter(
    "socket_io_messages_published", "Number of messages published by socketio"
)


@app.before_request
def before_request():
    """
    prometheus metrics for flask api
    """
    request.start_time = time.time()


@app.after_request
def increment_request_count(response):
    """
    prometheus metrics for flask api
    """
    request_latency = time.time() - request.start_time
    restful_api_request_latency.labels(request.method, request.path).observe(
        request_latency
    )
    restful_api_request_count.labels(
        request.method, request.path, response.status_code
    ).inc()
    return response


@app.route("/metrics")
def metrics():
    """
    serve the prometheus metrics
    """
    return make_wsgi_app()


class MarketSentiment(Resource):
    def get(self):
        try:
            target_date = request.args.get("date")
            validate_date(target_date)
        except ValueError as e:
            return (
                jsonify({"message": "invalid date, please use YYYY-MM-DD format"}),
                400,
            )

        try:
            news_sentiment = get_news_sentiment(target_date)
            return jsonify({"message": "success", "data": news_sentiment}), 200
        except Exception as e:
            logger.error(f"Error getting news sentiment: {e}")
            return jsonify({"message": "error", "data": {}}), 500


class MarketEmotion(Resource):
    def get(self):
        try:
            target_date = request.args.get("date")
            validate_date(target_date)
        except ValueError as e:
            return (
                jsonify({"message": "invalid date, please use YYYY-MM-DD format"}),
                400,
            )
        try:
            reddit_emotion = get_reddit_emotion(target_date)
            return jsonify({"message": "success", "data": reddit_emotion}), 200
        except Exception as e:
            logger.error(f"Error getting reddit emotion: {e}")
            return jsonify({"message": "error", "data": {}}), 500


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
        socket_io_messages_received.inc()
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
            socket_io_messages_published.inc()


@socketio.on("connect")
def handle_connect():
    socket_io_active_connections.inc()
    # start a background thread to listen to the kafka topic
    socketio.start_background_task(kafka_consumer)
    logger.info("socketio client connected")


@socketio.on("disconnect")
def handle_disconnect():
    socket_io_active_connections.dec()
    logger.info("socketio client disconnected")


api.add_resource(MarketSentiment, "/market_sentiment")
api.add_resource(MarketEmotion, "/market_emotion")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, allow_unsafe_werkzeug=True, debug=True)
