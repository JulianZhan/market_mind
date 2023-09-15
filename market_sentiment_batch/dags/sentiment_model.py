from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class AlphaVantageNewsWithSentiment(Base):
    __tablename__ = "alpha_vantage_news_with_sentiment"

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


class RedditCommentRaw(Base):
    __tablename__ = "reddit_comment_raw"

    id = Column(Integer, primary_key=True)
    comment = Column(String)


class RedditCommentClean(Base):
    __tablename__ = "reddit_comment_clean"

    id = Column(Integer, primary_key=True)
    comment = Column(String)


class Emotion(Base):
    __tablename__ = "emotion"

    id = Column(Integer, primary_key=True)
    emotion_name = Column(String)
    emotion_id = Column(Float)


class RedditCommentEmotion(Base):
    __tablename__ = "reddit_comment_emotion"

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("reddit_comment_clean.id"))
    emotion_id = Column(Integer, ForeignKey("emotion.id"))
    score = Column(Float)
