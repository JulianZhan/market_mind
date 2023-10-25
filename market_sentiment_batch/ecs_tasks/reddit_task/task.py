from datetime import timedelta
from reddit_utils import (
    get_reddit_comments_to_rds,
    get_reddit_comments_raw_to_clean,
    get_reddit_comments_clean_to_emotion,
    get_reddit_agg_to_db,
)

if __name__ == "__main__":
    first_inserted_at = get_reddit_comments_to_rds(
        "CryptoCurrency", post_limit=100, batch_size=300
    )
    first_inserted_at = get_reddit_comments_raw_to_clean(
        first_inserted_at, batch_size=300
    )
    first_inserted_at = get_reddit_comments_clean_to_emotion(first_inserted_at, 20, 300)
    get_reddit_agg_to_db()
