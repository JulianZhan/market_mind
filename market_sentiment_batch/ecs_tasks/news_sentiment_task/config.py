from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

    RDS_HOSTNAME = os.getenv("RDS_HOSTNAME")
    RDS_USER = os.getenv("RDS_USER")
    RDS_PASSWORD = os.getenv("RDS_PASSWORD")
    RDS_DB_NAME = os.getenv("RDS_DB_NAME")
