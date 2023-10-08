from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    """
    Config class to store all the environment variables

    Attributes:
        FINNHUB_API_KEY: str
        KAFAK_SERVER: str
        KAFKA_PORT: str
        KAFKA_TOPIC_NAME: str
    """

    FINNHUB_API_KEY: str = os.getenv("FINNHUB_API_KEY")

    KAFAK_SERVER: str = os.getenv("KAFKA_SERVER")
    KAFKA_PORT: str = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC_NAME: str = os.getenv("KAFKA_TOPIC_NAME")
