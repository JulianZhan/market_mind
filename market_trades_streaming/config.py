from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
    KAFAK_SERVER = os.getenv("KAFKA_SERVER")
    KAFKA_PORT = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME")
