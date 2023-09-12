import requests
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import Config
from datetime import datetime, timedelta


# Connect to the database
DATABASE_URL = f"mysql+mysqlconnector://{Config.RDS_USER}:{Config.RDS_PASSWORD}@{Config.RDS_HOSTNAME}/{Config.RDS_DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
MAX_NEWS_ITEMS = 1000
time_from = (datetime.now() - timedelta(days=1)).strftime("%Y%m%dT%H%M")

url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&time_from={time_from}&limit={MAX_NEWS_ITEMS}&apikey={Config.ALPHAVANTAGE_API_KEY}"
r = requests.get(url)
data = r.json()
data["feed"]
data["items"]


Base = declarative_base()


class AlphaVantageNewsSentiment(Base):
    __tablename__ = "alpha_vantage_news_sentiment"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    time_published = Column(DateTime)
    authors = Column(String)
    summary = Column(String)
    banner_image = Column(String)
    source = Column(String)
    category_within_source = Column(String)
    source_domain = Column(String)
    overall_sentiment_score = Column(Float)
    overall_sentiment_label = Column(String)

    topics = relationship("Topic", back_populates="article")
    ticker_sentiments = relationship("TickerSentiment", back_populates="article")


# Sample data (as provided)
data = [...]  # Your data here

# Insert data using ORM
with Session() as session:
    articles = []
    for article_data in data:
        article = Article(
            title=article_data["title"],
            url=article_data["url"],
            time_published=article_data["time_published"],
            authors=", ".join(article_data["authors"]),
            summary=article_data["summary"],
            banner_image=article_data["banner_image"],
            source=article_data["source"],
            category_within_source=article_data["category_within_source"],
            source_domain=article_data["source_domain"],
            overall_sentiment_score=article_data["overall_sentiment_score"],
            overall_sentiment_label=article_data["overall_sentiment_label"],
            topics=[
                Topic(topic=t["topic"], relevance_score=t["relevance_score"])
                for t in article_data["topics"]
            ],
            ticker_sentiments=[
                TickerSentiment(
                    ticker=t["ticker"],
                    relevance_score=t["relevance_score"],
                    ticker_sentiment_score=t["ticker_sentiment_score"],
                    ticker_sentiment_label=t["ticker_sentiment_label"],
                )
                for t in article_data.get("ticker_sentiment", [])
            ],
        )
        articles.append(article)

    session.bulk_save_objects(articles)
    session.commit()
