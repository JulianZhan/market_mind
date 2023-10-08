from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()


class Config:
    """
    Config class to store environment variables

    Attributes:
        KAFAK_SERVER (Optional[str]): kafka server
        KAFKA_PORT (Optional[str]): kafka port
        KAFKA_TOPIC_NAME (Optional[str]): kafka topic name
        RDS_HOSTNAME (Optional[str]): RDS hostname
        RDS_USER (Optional[str]): RDS username
        RDS_PASSWORD (Optional[str]): RDS password
        RDS_DB_NAME (Optional[str]): RDS database name
        RDS_PORT (Optional[str]): RDS port
    """

    KAFAK_SERVER: Optional[str] = os.getenv("KAFKA_SERVER")
    KAFKA_PORT: Optional[str] = os.getenv("KAFKA_PORT")
    KAFKA_TOPIC_NAME: Optional[str] = os.getenv("KAFKA_TOPIC_NAME")

    RDS_HOSTNAME: Optional[str] = os.getenv("RDS_HOSTNAME")
    RDS_USER: Optional[str] = os.getenv("RDS_USER")
    RDS_PASSWORD: Optional[str] = os.getenv("RDS_PASSWORD")
    RDS_DB_NAME: Optional[str] = os.getenv("RDS_DB_NAME")
    RDS_PORT: Optional[str] = os.getenv("RDS_PORT")
