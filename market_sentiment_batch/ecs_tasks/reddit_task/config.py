from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    """
    Config class to store environment variables

    Attributes:
        REDDIT_CLIENT_ID: str
        REDDIT_CLIENT_SECRET: str
        REDDIT_USERNAME: str
        REDDIT_PASSWORD: str
        REDDIT_USER_AGENT: str
        RDS_HOSTNAME: str
        RDS_USER: str
        RDS_PASSWORD: str
        RDS_DB_NAME: str
        MODEL_ENDPOINT: str
    """

    REDDIT_CLIENT_ID: str = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET: str = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USERNAME: str = os.getenv("REDDIT_USERNAME")
    REDDIT_PASSWORD: str = os.getenv("REDDIT_PASSWORD")
    REDDIT_USER_AGENT: str = os.getenv("REDDIT_USER_AGENT")

    RDS_HOSTNAME: str = os.getenv("RDS_HOSTNAME")
    RDS_USER: str = os.getenv("RDS_USER")
    RDS_PASSWORD: str = os.getenv("RDS_PASSWORD")
    RDS_DB_NAME: str = os.getenv("RDS_DB_NAME")

    MODEL_ENDPOINT: str = os.getenv("MODEL_ENDPOINT")
