from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    BigInteger,
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class AlphaVantageNewsWithSentiment(Base):
    __tablename__ = "alpha_vantage_news_with_sentiment"

    id = Column(BigInteger, primary_key=True)
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


class AlphaVantageAgg(Base):
    __tablename__ = "alpha_vantage_agg"

    id = Column(BigInteger, primary_key=True)
    date_recorded = Column(DateTime, unique=True)
    avg_score = Column(Float)
    max_score = Column(Float)
    min_score = Column(Float)
    std_score = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
