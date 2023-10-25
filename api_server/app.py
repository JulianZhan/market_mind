from flask import Flask, request, jsonify, make_response
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

# global variables for kafka consumer
kafka_consumer_settings = {
    "bootstrap.servers": f"{Config.KAFAK_SERVER}:{Config.KAFKA_PORT}",
    "group.id": "market_trades_streaming_serving",
    "auto.offset.reset": "latest",
}


# set up flask app, api and socketio
app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app)


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
            return make_response(
                jsonify({"message": "invalid date, please use YYYY-MM-DD format"}),
                400,
            )

        try:
            news_sentiment = get_news_sentiment(target_date)
            return make_response(
                jsonify({"message": "success", "data": news_sentiment}), 200
            )
        except Exception as e:
            logger.error(f"Error getting news sentiment: {e}")
            return make_response(jsonify({"message": "error", "data": {}}), 500)


class MarketEmotion(Resource):
    def get(self):
        try:
            target_date = request.args.get("date")
            validate_date(target_date)
        except ValueError as e:
            return make_response(
                jsonify({"message": "invalid date, please use YYYY-MM-DD format"}),
                400,
            )
        try:
            reddit_emotion = get_reddit_emotion(target_date)
            return make_response(
                jsonify({"message": "success", "data": reddit_emotion}), 200
            )
        except Exception as e:
            logger.error(f"Error getting reddit emotion: {e}")
            return make_response(jsonify({"message": "error", "data": {}}), 500)


def kafka_consumer():
    """
    continuously listen to the kafka topic and emit the message to the socketio client
    """

    # set up kafka consumer
    consumer = Consumer(kafka_consumer_settings)
    consumer.subscribe([Config.KAFKA_TOPIC_NAME])
    poll_interval = 1.0
    while True:
        # consumer will fetch the message received in the last {poll_interval} second from the kafka topic
        msg = consumer.poll(poll_interval)
        # if no message received, continue
        if msg is None:
            continue
        # if error in the message, log the error
        if msg.error():
            logger.error(f"Consumer error: {msg.error()}")
            continue
        # if no error in the message, decode the message and emit to the socketio client
        else:
            socket_io_messages_received.inc()
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
