from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    BigInteger,
    UniqueConstraint,
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


class RedditCommentRaw(Base):
    __tablename__ = "reddit_comment_raw"

    id = Column(BigInteger, primary_key=True)
    comment = Column(String)
    created_at = Column(DateTime)


class RedditCommentClean(Base):
    __tablename__ = "reddit_comment_clean"

    id = Column(BigInteger, primary_key=True)
    comment = Column(String)
    created_at = Column(DateTime)


class Emotion(Base):
    __tablename__ = "emotion"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)


class RedditCommentEmotion(Base):
    __tablename__ = "reddit_comment_emotion"

    id = Column(BigInteger, primary_key=True)
    comment_id = Column(BigInteger, ForeignKey("reddit_comment_clean.id"))
    emotion_id = Column(BigInteger, ForeignKey("emotion.id"))
    score = Column(Float)
    created_at = Column(DateTime)


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
