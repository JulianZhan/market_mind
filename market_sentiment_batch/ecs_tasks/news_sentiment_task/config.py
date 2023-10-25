from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    """
    Config class to store environment variables

    Attributes:
        ALPHAVANTAGE_API_KEY: str
        RDS_HOSTNAME: str
        RDS_USER: str
        RDS_PASSWORD: str
        RDS_DB_NAME: str
    """

    ALPHAVANTAGE_API_KEY: str = os.getenv("ALPHAVANTAGE_API_KEY")

    RDS_HOSTNAME: str = os.getenv("RDS_HOSTNAME")
    RDS_USER: str = os.getenv("RDS_USER")
    RDS_PASSWORD: str = os.getenv("RDS_PASSWORD")
    RDS_DB_NAME: str = os.getenv("RDS_DB_NAME")
