from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()


class Config:
    """
    Config class to store environment variables

    Attributes:
        FINNHUB_API_KEY (Optional[str]): finnhub api key
        KAFAK_SERVER (Optional[str]): kafka server
        KAFKA_PORT (Optional[str]): kafka port
        KAFKA_TOPIC_NAME (Optional[str]): kafka topic name
    """

    FINNHUB_API_KEY: Optional[str] = os.getenv("FINNHUB_API_KEY")

    KAFAK_SERVER: Optional[str] = os.getenv("KAFKA_SERVER")
    KAFKA_PORT: Optional[str] = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC_NAME: Optional[str] = os.getenv("KAFKA_TOPIC_NAME")
