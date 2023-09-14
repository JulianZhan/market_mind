import requests
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from config import Config
from datetime import datetime, timedelta
from sentiment_model import AlphaVantageNewsSentiment
import logging


# Connect to the database
database_url = f"mysql+mysqlconnector://{Config.RDS_USER}:{Config.RDS_PASSWORD}@{Config.RDS_HOSTNAME}/{Config.RDS_DB_NAME}"
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
max_news_items = 1000
time_from = (datetime.now() - timedelta(days=1)).strftime("%Y%m%dT%H%M")
url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&time_from={time_from}&limit={max_news_items}&apikey={Config.ALPHAVANTAGE_API_KEY}"
# set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def get_news_sentiment_data(url):
    res = requests.get(url)
    try:
        json_data = res.json()  # Convert response to JSON

        if res.status_code != 200:
            logger.error(
                f"Failed to get data from {url}, status code: {res.status_code}, response: {res.text}"
            )
            return None
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
    with Session() as session:
        for i in range(0, len(data), batch_size):
            news_sentiment_list = []
            batch = data[i : i + batch_size]

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

            session.execute(insert(AlphaVantageNewsSentiment), news_sentiment_list)
            session.commit()
