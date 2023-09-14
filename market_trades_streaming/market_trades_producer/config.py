from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
    KAFAK_SERVER = os.getenv("KAFKA_SERVER")
    KAFKA_PORT = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME")

    RDS_HOSTNAME = os.getenv("RDS_HOSTNAME")
    RDS_USER = os.getenv("RDS_USER")
    RDS_PASSWORD = os.getenv("RDS_PASSWORD")
    RDS_DB_NAME = os.getenv("RDS_DB_NAME")
    RDS_PORT = os.getenv("RDS_PORT")
