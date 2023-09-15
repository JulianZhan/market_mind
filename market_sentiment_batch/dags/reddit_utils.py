import re
import praw
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from config import Config
from sentiment_model import (
    RedditCommentRaw,
    RedditCommentClean,
    RedditCommentEmotion,
    Emotion,
)
import logging
from transformers import pipeline

# set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Connect to the database
DATABASE_URL = f"mysql+mysqlconnector://{Config.RDS_USER}:{Config.RDS_PASSWORD}@{Config.RDS_HOSTNAME}/{Config.RDS_DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


# load the sentiment model, which trains on reddit and twitter data
classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True,
)

# set up reddit api
reddit = praw.Reddit(
    client_id=Config.REDDIT_CLIENT_ID,
    client_secret=Config.REDDIT_CLIENT_SECRET,
    username=Config.REDDIT_USERNAME,
    password=Config.REDDIT_PASSWORD,
    user_agent=Config.REDDIT_USER_AGENT,
)


def get_new_reddit_comments(subreddit_name, limit):
    return reddit.subreddit(subreddit_name).new(limit=limit)


def generic_batch_insert(session, model, data, batch_size):
    """
    generic batch insert function

    Args:
        session (sqlalchemy.orm.session.Session): the session object
        model (sqlalchemy.ext.declarative.api.DeclarativeMeta): the model class
        data (list): the data to insert
        batch_size (int): the batch size

    Returns:
        int: the id of the first inserted row
    """
    latest_inserted_ids = []
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        inserted_ids = session.execute(insert(model).returning(model.id), batch)
        latest_inserted_ids.append(inserted_ids.fetchone()[0])
    session.commit()
    return min(latest_inserted_ids)


def batch_insert_reddit_comments_raw(data, batch_size):
    """
    insert reddit comments into database in batches

    Args:
        data (list): reddit comments in list of dictionary format
        batch_size (int): number of rows to insert into database in each batch

    Returns:
        int: the id of the first inserted row
    """
    # open a session with orm
    with Session() as session:
        comments_list = []
        for post in data:
            post.comments.replace_more(limit=1)
            for comment_data in post.comments:
                comments_list.append({"comment": comment_data.body})
        return generic_batch_insert(
            session, RedditCommentRaw, comments_list, batch_size
        )


def fetch_comments_after_id(model, first_inserted_id):
    """
    Fetch all model records with ID greater than the given ID.

    Args:
        first_inserted_id (int): The starting ID.

    Returns:
        List of model instances with ID greater than first_inserted_id.
    """
    with Session() as session:
        # Query the model table for all entries with ID greater than first_inserted_id
        comments = session.query(model).filter(model.id >= first_inserted_id).all()

    return comments


def clean_comment(text):
    """
    clean the reddit comment text

    Args:
        text (str): the text of the reddit comment

    Returns:
        str: the cleaned text of the reddit comment
    """
    try:
        # remove [deleted] and [removed]
        text = re.sub(r"\[deleted\]|\[removed\]", "", text)
        # remove urls
        text = re.sub(r"http\S+", "", text)
        # remove mentions (words starting with '@' or '/u/')
        text = re.sub(r"@\S+|/u/\S+", "", text)
        # remove special characters and numbers
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        # convert to lowercase
        text = text.lower()
        # remove extra spaces
        text = " ".join(text.split())

        return text
    except Exception as e:
        logger.error(f"Failed to clean comment: {e}, comment: {text}")
        return ""


def batch_insert_reddit_comments_clean(data, batch_size):
    """
    clean and insert reddit comments into database in batches

    Args:
        data (list): reddit comments in list of dictionary format
        batch_size (int): number of rows to insert into database in each batch

    Returns:
        int: the id of the first inserted row
    """
    # open a session with orm
    with Session() as session:
        cleaned_comments_list = [
            {"comment": clean_comment(comment.comment)} for comment in data
        ]
        return generic_batch_insert(
            session, RedditCommentClean, cleaned_comments_list, batch_size
        )


def batch_predict_emotion(data, batch_size):
    """
    batch predict emotion for clean reddit comments

    Args:
        data (list): reddit comments in list of dictionary format
        batch_size (int): number of rows to insert into database in each batch

    Returns:
        list: list of tuples of (comment_id, predictions)
    """
    results = []
    for i in range(0, len(data), batch_size):
        batch_comments_data = data[i : i + batch_size]
        batch_comments = [comment["comment"] for comment in batch_comments_data]
        batch_ids = [comment["id"] for comment in batch_comments_data]
        batch_predictions = classifier(batch_comments)
        results.extend(zip(batch_ids, batch_predictions))
    return results


def result_emotion_name_to_id(result):
    """
    convert emotion name to emotion id

    Args:
        result (list): list of tuples of (comment_id, predictions)

    Returns:
        list: list of tuples of (comment_id, predictions)
    """
    with Session() as session:
        emotions = session.query(Emotion).all()
        emotion_name_to_id = {emotion.name: emotion.id for emotion in emotions}
    return [
        (
            comment_id,
            [
                {"label": emotion_name_to_id[pred["label"]], "score": pred["score"]}
                for pred in predictions
            ],
        )
        for comment_id, predictions in result
    ]


def batch_insert_reddit_comments_emotion(data, batch_size):
    """
    batch insert reddit comments emotion

    Args:
        data (list): reddit comments in list of dictionary format
        batch_size (int): number of rows to insert into database in each batch

    Returns:
        int: the id of the first inserted row
    """

    # open a session with orm
    with Session() as session:
        emotion_list = []
        for comment, predictions in data:
            for prediction in predictions:
                emotion_list.append(
                    {
                        "comment_id": comment.id,
                        "emotion_id": prediction["label"],
                        "score": prediction["score"],
                    }
                )
        return generic_batch_insert(
            session, RedditCommentEmotion, emotion_list, batch_size
        )


def get_reddit_comments_to_rds(subreddit_name, post_limit, batch_size):
    data = get_new_reddit_comments(subreddit_name, post_limit)
    first_inserted_id = batch_insert_reddit_comments_raw(data, batch_size)
    return first_inserted_id


def get_reddit_comments_raw_to_clean(first_inserted_id, batch_size):
    comments = fetch_comments_after_id(RedditCommentRaw, first_inserted_id)
    first_inserted_id = batch_insert_reddit_comments_clean(comments, batch_size)
    return first_inserted_id


def get_reddit_comments_clean_to_emotion(
    first_inserted_id, batch_size_for_prediction, batch_size_for_insert
):
    comments = fetch_comments_after_id(RedditCommentClean, first_inserted_id)
    predictions = batch_predict_emotion(comments, batch_size_for_prediction)
    predictions_with_emotion_id = result_emotion_name_to_id(predictions)
    first_inserted_id = batch_insert_reddit_comments_emotion(
        predictions_with_emotion_id, batch_size_for_insert
    )
    return first_inserted_id
