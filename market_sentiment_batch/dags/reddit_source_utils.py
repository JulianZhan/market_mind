import re
import praw
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from config import Config
from config import Config
from sentiment_model import RedditComment

# Connect to the database
DATABASE_URL = f"mysql+mysqlconnector://{Config.RDS_USER}:{Config.RDS_PASSWORD}@{Config.RDS_HOSTNAME}/{Config.RDS_DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

reddit = praw.Reddit(
    client_id=Config.REDDIT_CLIENT_ID,
    client_secret=Config.REDDIT_CLIENT_SECRET,
    username=Config.REDDIT_USERNAME,
    password=Config.REDDIT_PASSWORD,
    user_agent=Config.REDDIT_USER_AGENT,
)


def clean_comment(text):
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


new_posts = reddit.subreddit("stocks").new(limit=10)


def batch_insert_reddit_comments(data, batch_size):
    """
    insert reddit comments into database in batches

    Args:
        data (list): reddit comments in list of dictionary format
        batch_size (int): number of rows to insert into database in each batch
    """
    # open a session with orm
    with Session() as session:
        for i in range(0, len(data), batch_size):
            # for each batch of data, use slice to get the target batch
            comments_list = []
            batch = data[i : i + batch_size]

            for post in batch:
                # fetch the top-level comments
                post.comments.replace_more(limit=1)
                for comment_data in post.comments:
                    comment = {"comment": comment_data.body}
                    comments_list.append(comment)

            # bulk insert the batch of data into database
            session.execute(insert(RedditComment), comments_list)
        session.commit()
