import requests
from sqlalchemy import create_engine, insert, func
from sqlalchemy.orm import sessionmaker
from config import Config
from datetime import datetime, timedelta
from sentiment_model import AlphaVantageNewsWithSentiment, AlphaVantageAgg
import logging


# connect to the database
database_url = f"mysql+mysqlconnector://{Config.RDS_USER}:{Config.RDS_PASSWORD}@{Config.RDS_HOSTNAME}/{Config.RDS_DB_NAME}"
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
# set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def get_news_sentiment_data(url: str) -> list:
    """
    get news sentiment data from Alpha Vantage API

    Args:
        url (str): url to get news sentiment data from, with query parameters

    Returns:
        list: news sentiment data in list of dictionary format
    """
    res = requests.get(url)
    try:
        json_data = res.json()  # Convert response to JSON

        if res.status_code != 200:
            logger.error(
                f"Failed to get data from {url}, status code: {res.status_code}, response: {res.text}"
            )
            return None
        # if no news items found, return None
        elif "items" in json_data and json_data["items"] == 0:
            logger.info(f"No news items found for url: {url}, response: {res.text}")
            return None
        else:
            logger.info(f"Successfully retrieved data from {url}")
            return json_data["feed"]
    except Exception as e:
        logger.error(f"Failed to get data from {url}, error: {e}")
        return None


def parse_news_sentiment_data(data: dict) -> dict:
    """
    parse data to dictionary format for database insertion

    Args:
        data (dict): news sentiment data from Alpha Vantage API

    Returns:
        dict: news sentiment data in dictionary format
    """

    news_sentiment = {
        "title": data["title"],
        "url": data["url"],
        "time_published": data["time_published"],
        "summary": data["summary"],
        "banner_image": data["banner_image"],
        "source": data["source"],
        "category_within_source": data["category_within_source"],
        "source_domain": data["source_domain"],
        "overall_sentiment_score": data["overall_sentiment_score"],
        "overall_sentiment_label": data["overall_sentiment_label"],
    }
    return news_sentiment


def batch_insert_news_sentiment_data(data: list, batch_size: int):
    """
    insert news sentiment data into database in batches

    Args:
        data (list): news sentiment data in list of dictionary format
        batch_size (int): number of rows to insert into database in each batch
    """
    # open a session with orm
    with Session() as session:
        try:
            # for each batch of data, use slice to get the target batch
            for i in range(0, len(data), batch_size):
                news_sentiment_list = []
                batch = data[i : i + batch_size]

                # collect the data to be inserted as a list of dictionary
                for news_sentiment_data in batch:
                    news_sentiment = parse_news_sentiment_data(news_sentiment_data)
                    news_sentiment_list.append(news_sentiment)

                # bulk insert the data into database
                session.execute(
                    insert(AlphaVantageNewsWithSentiment), news_sentiment_list
                )
            session.commit()
        except Exception as e:
            logger.error(
                f"Failed to insert data into database, error: {e}, data: {data}"
            )
            session.rollback()


def save_news_sentiment_data_to_db(url: str, batch_size: int):
    """
    combine get_news_sentiment_data and batch_insert_news_sentiment_data functions
    save news sentiment data to database

    Args:
        url (str): url to get news sentiment data from, with query parameters
        batch_size (int): number of rows to insert into database in each batch
    """
    data = get_news_sentiment_data(url)

    # if data is None, it implicates that no news items are found
    if data is not None:
        batch_insert_news_sentiment_data(data, batch_size)
        logger.info("Successfully inserted data into database")
    else:
        logger.info("No data to insert into database")


def calculate_news_agg():
    """
    calculate news sentiment aggregation from alpha_vantage_news_with_sentiment table

    Returns:
        list: news sentiment aggregation in list format, each row is a tuple
    """
    with Session() as session:
        try:
            three_days_ago = (datetime.utcnow() - timedelta(days=3)).isoformat(
                timespec="seconds"
            )
            return (
                session.query(
                    func.date(AlphaVantageNewsWithSentiment.created_at).label(
                        "date_recorded"
                    ),
                    func.avg(
                        AlphaVantageNewsWithSentiment.overall_sentiment_score
                    ).label("avg_score"),
                    func.max(
                        AlphaVantageNewsWithSentiment.overall_sentiment_score
                    ).label("max_score"),
                    func.min(
                        AlphaVantageNewsWithSentiment.overall_sentiment_score
                    ).label("min_score"),
                    func.stddev(
                        AlphaVantageNewsWithSentiment.overall_sentiment_score
                    ).label("std_score"),
                )
                .filter(AlphaVantageNewsWithSentiment.created_at >= three_days_ago)
                .group_by(func.date(AlphaVantageNewsWithSentiment.created_at))
            ).all()
        except Exception as e:
            logger.error(f"Failed to calculate news agg: {e}")
            return None


def save_news_agg_to_db():
    """
    save news sentiment aggregation to database
    """
    news_agg = calculate_news_agg()
    with Session() as session:
        try:
            # the data size of news_agg is pretty small, so we use basic method to insert data to improve readability and maintainability
            for row in news_agg:
                # insert on duplicate key update, if the date_recorded already exists, update the other columns
                existing = (
                    session.query(AlphaVantageAgg)
                    .filter_by(date_recorded=row.date_recorded)
                    .first()
                )
                if existing:
                    existing.avg_score = row.avg_score
                    existing.max_score = row.max_score
                    existing.min_score = row.min_score
                    existing.std_score = row.std_score
                else:
                    # if the date_recorded does not exist, insert a new row
                    new_agg = {
                        "date_recorded": row.date_recorded,
                        "avg_score": row.avg_score,
                        "max_score": row.max_score,
                        "min_score": row.min_score,
                        "std_score": row.std_score,
                    }
                    session.execute(insert(AlphaVantageAgg), new_agg)

            session.commit()
            logger.info("Successfully inserted data into database")
        except Exception as e:
            logger.error(f"Failed to insert data into database, error: {e}")
            session.rollback()
