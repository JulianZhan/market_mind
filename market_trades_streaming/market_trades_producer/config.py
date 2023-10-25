from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    """
    Config class to store all the environment variables

    Attributes:
        POLYGON_API_KEY: str
        KAFKA_SERVER: str
        KAFKA_PORT: str
        KAFKA_TOPIC_NAME: str
    """

    POLYGON_API_KEY: str = os.getenv("POLYGON_API_KEY")

    KAFKA_SERVER: str = os.getenv("KAFKA_SERVER")
    KAFKA_PORT: str = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC_NAME: str = os.getenv("KAFKA_TOPIC_NAME")
