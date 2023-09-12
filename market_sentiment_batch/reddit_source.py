import praw
from config import Config

reddit = praw.Reddit(
    client_id=Config.REDDIT_CLIENT_ID,
    client_secret=Config.REDDIT_CLIENT_SECRET,
    username=Config.REDDIT_USERNAME,
    password=Config.REDDIT_PASSWORD,
    user_agent=Config.REDDIT_USER_AGENT,
)

subreddit = reddit.subreddit("CryptoCurrency")
r = subreddit.hot(limit=100)
hot_posts = reddit.subreddit("stocks").new(limit=2)
for post in hot_posts:
    print(post.title)  # Print the title of the post
    i = 0
    # Fetch the top-level comments
    post.comments.replace_more(
        limit=1
    )  # This line ensures you get all top-level comments
    for comment in post.comments:
        print(comment.body)  # Print the content of the comment
        i += 1
