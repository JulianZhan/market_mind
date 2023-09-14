import requests
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from config import Config
from sentiment_model import AlphaVantageNewsWithSentiment
import logging


# Connect to the database
database_url = f"mysql+mysqlconnector://{Config.RDS_USER}:{Config.RDS_PASSWORD}@{Config.RDS_HOSTNAME}/{Config.RDS_DB_NAME}"
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
# set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def get_news_sentiment_data(url):
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


def batch_insert_news_sentiment_data(data, batch_size):
    """
    insert news sentiment data into database in batches

    Args:
        data (list): news sentiment data in list of dictionary format
        batch_size (int): number of rows to insert into database in each batch
    """
    # open a session with orm
    with Session() as session:
        # for each batch of data, use slice to get the target batch
        for i in range(0, len(data), batch_size):
            news_sentiment_list = []
            batch = data[i : i + batch_size]

            # collect the data to be inserted as a list of dictionary
            for news_sentiment_data in batch:
                news_sentiment = {
                    "title": news_sentiment_data["title"],
                    "url": news_sentiment_data["url"],
                    "time_published": news_sentiment_data["time_published"],
                    "summary": news_sentiment_data["summary"],
                    "banner_image": news_sentiment_data["banner_image"],
                    "source": news_sentiment_data["source"],
                    "category_within_source": news_sentiment_data[
                        "category_within_source"
                    ],
                    "source_domain": news_sentiment_data["source_domain"],
                    "overall_sentiment_score": news_sentiment_data[
                        "overall_sentiment_score"
                    ],
                    "overall_sentiment_label": news_sentiment_data[
                        "overall_sentiment_label"
                    ],
                }
                news_sentiment_list.append(news_sentiment)

            # bulk insert the data into database
            session.execute(insert(AlphaVantageNewsWithSentiment), news_sentiment_list)
        session.commit()


def save_news_sentiment_data_to_db(url, batch_size):
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
