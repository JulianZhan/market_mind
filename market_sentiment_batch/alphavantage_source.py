import requests
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config
from datetime import datetime, timedelta
from sentiment_model import AlphaVantageNewsSentiment


# Connect to the database
DATABASE_URL = f"mysql+mysqlconnector://{Config.RDS_USER}:{Config.RDS_PASSWORD}@{Config.RDS_HOSTNAME}/{Config.RDS_DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
MAX_NEWS_ITEMS = 1000
time_from = (datetime.now() - timedelta(days=1)).strftime("%Y%m%dT%H%M")

url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&time_from={time_from}&limit={MAX_NEWS_ITEMS}&apikey={Config.ALPHAVANTAGE_API_KEY}"
res = requests.get(url)
data = res.json()["feed"]
Base = declarative_base()

with Session() as session:
    news_sentiment_list = []
    for news_sentiment_data in data:
        news_sentiment = AlphaVantageNewsSentiment(
            title=news_sentiment_data["title"],
            url=news_sentiment_data["url"],
            time_published=news_sentiment_data["time_published"],
            summary=news_sentiment_data["summary"],
            banner_image=news_sentiment_data["banner_image"],
            source=news_sentiment_data["source"],
            category_within_source=news_sentiment_data["category_within_source"],
            source_domain=news_sentiment_data["source_domain"],
            overall_sentiment_score=news_sentiment_data["overall_sentiment_score"],
            overall_sentiment_label=news_sentiment_data["overall_sentiment_label"],
        )
        news_sentiment_list.append(news_sentiment)

    session.bulk_save_objects(news_sentiment_list)
    session.commit()
