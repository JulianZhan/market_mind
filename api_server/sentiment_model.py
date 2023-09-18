from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    BigInteger,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Emotion(Base):
    __tablename__ = "emotion"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)


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


class RedditAgg(Base):
    __tablename__ = "reddit_agg"

    id = Column(BigInteger, primary_key=True)
    date_recorded = Column(DateTime)
    emotion_name = Column(String(55))
    avg_score = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    __table_args__ = (
        UniqueConstraint(
            "date_recorded", "emotion_name", name="uc_reddit_date_emotion"
        ),
    )
