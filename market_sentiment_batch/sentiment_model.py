from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class AlphaVantageNewsSentiment(Base):
    __tablename__ = "alpha_vantage_news_sentiment"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    time_published = Column(DateTime)
    summary = Column(String)
    banner_image = Column(String)
    source = Column(String)
    category_within_source = Column(String)
    source_domain = Column(String)
    overall_sentiment_score = Column(Float)
    overall_sentiment_label = Column(String)
