from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
    REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

    RDS_HOSTNAME = os.getenv("RDS_HOSTNAME")
    RDS_USER = os.getenv("RDS_USER")
    RDS_PASSWORD = os.getenv("RDS_PASSWORD")
    RDS_DB_NAME = os.getenv("RDS_DB_NAME")

    MODEL_ENDPOINT = os.getenv("MODEL_ENDPOINT")
