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
