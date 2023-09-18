from sentiment_model import AlphaVantageAgg, RedditAgg
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import logging
from config import Config
import datetime


# set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Connect to the database
DATABASE_URL = f"mysql+mysqlconnector://{Config.RDS_USER}:{Config.RDS_PASSWORD}@{Config.RDS_HOSTNAME}/{Config.RDS_DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def validate_date(date_text):
    datetime.date.fromisoformat(date_text)


def get_news_sentiment(target_date):
    with Session() as session:
        news_sentiment = (
            session.query(
                AlphaVantageAgg.avg_score,
                AlphaVantageAgg.max_score,
                AlphaVantageAgg.min_score,
                AlphaVantageAgg.std_score,
            )
            .filter(func.date(AlphaVantageAgg.date_recorded) == target_date)
            .first()
        )
        news_sentiment = {
            "score_definition": {
                "Bearish": "score <= -0.35",
                "Somewhat-Bearish": "-0.35 < score <= -0.15",
                "Neutral": "-0.15 < score < 0.15",
                "Somewhat-Bullish": "0.15 <= score < 0.35",
                "Bullish": "score >= 0.35",
            },
            "score": {
                "avg_score": news_sentiment.avg_score,
                "max_score": news_sentiment.max_score,
                "min_score": news_sentiment.min_score,
                "std_score": news_sentiment.std_score,
            },
            "date_recorded": target_date,
        }
        return news_sentiment


def get_reddit_emotion(target_date):
    with Session() as session:
        reddit_emotion = (
            session.query(RedditAgg)
            .filter(func.date(RedditAgg.date_recorded) == target_date)
            .all()
        )
