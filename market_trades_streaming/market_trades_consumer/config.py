from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()


class Config:
    """
    Config class to store all the environment variables

    Attributes:
        KAFAK_SERVER: str
        KAFKA_PORT: str
        KAFKA_TOPIC_NAME: str
        RDS_HOSTNAME: str
        RDS_USER: str
        RDS_PASSWORD: str
        RDS_DB_NAME: str
        RDS_PORT: str
    """

    KAFAK_SERVER: str = os.getenv("KAFKA_SERVER")
    KAFKA_PORT: str = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC_NAME: str = os.getenv("KAFKA_TOPIC_NAME")

    RDS_HOSTNAME: str = os.getenv("RDS_HOSTNAME")
    RDS_USER: str = os.getenv("RDS_USER")
    RDS_PASSWORD: str = os.getenv("RDS_PASSWORD")
    RDS_DB_NAME: str = os.getenv("RDS_DB_NAME")
    RDS_PORT: str = os.getenv("RDS_PORT")