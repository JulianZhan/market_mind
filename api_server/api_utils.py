from sentiment_model import AlphaVantageAgg, RedditAgg
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import logging
from config import Config
import datetime
import avro.schema
import avro.io
import io


# set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# connect to the database
DATABASE_URL = f"mysql+mysqlconnector://{Config.RDS_USER}:{Config.RDS_PASSWORD}@{Config.RDS_HOSTNAME}/{Config.RDS_DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
# avro schema for the kafka message
avro_schema = avro.schema.parse(open("trades_schema.avsc", "r").read())
# score definition
score_definition = {
    "Bearish": "score <= -0.35",
    "Somewhat-Bearish": "-0.35 < score <= -0.15",
    "Neutral": "-0.15 < score < 0.15",
    "Somewhat-Bullish": "0.15 <= score < 0.35",
    "Bullish": "score >= 0.35",
}


def decode_avro_message(message, schema) -> dict:
    """
    decode the avro message from kafka

    Args:
        message: message from kafka
        schema (avro.schema): avro schema

    Returns:
        dict: decoded message
    """
    # initialize a bytes reader convert the message to readable bytes stream
    bytes_reader = io.BytesIO(message)
    # create a binary decoder to decode the message
    decoder = avro.io.BinaryDecoder(bytes_reader)
    # create a datum reader to read the message
    reader = avro.io.DatumReader(schema)
    # actual decoding
    return reader.read(decoder)


def validate_date(date_text: str) -> bool:
    """
    try to convert the date string to date object
    if failed, error will be raised
    """
    datetime.date.fromisoformat(date_text)


def get_news_sentiment(target_date: str) -> dict:
    """
    get the news sentiment for the target date

    Args:
        target_date (str): target date in YYYY-MM-DD format

    Returns:
        dict: news sentiment
    """
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
        news_sentiment_dict = {
            "score_definition": score_definition,
            "score": {
                "avg_score": news_sentiment.avg_score,
                "max_score": news_sentiment.max_score,
                "min_score": news_sentiment.min_score,
                "std_score": news_sentiment.std_score,
            },
            "date_recorded": target_date,
        }
        return news_sentiment_dict


def transform_reddit_emotion(reddit_emotion, target_date: str) -> dict:
    # transform the reddit emotion from sqlalchemy object to dict
    reddit_emotion_dict = {"emotion": {}, "date_recorded": target_date}
    # for each emotion in the target date, add it to the dict
    for emotion in reddit_emotion:
        reddit_emotion_dict["emotion"][emotion.emotion_name] = emotion.avg_score
    return reddit_emotion_dict


def get_reddit_emotion(target_date: str) -> dict:
    """
    get reddit emotion for the target date

    Args:
        target_date (str): target date in YYYY-MM-DD format

    Returns:
        dict: reddit emotion
    """
    with Session() as session:
        reddit_emotion = (
            session.query(RedditAgg)
            .filter(func.date(RedditAgg.date_recorded) == target_date)
            .all()
        )
        reddit_emotion_dict = transform_reddit_emotion(reddit_emotion, target_date)
        return reddit_emotion_dict
