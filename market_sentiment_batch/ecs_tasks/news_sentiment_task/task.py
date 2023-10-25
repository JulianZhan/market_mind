from datetime import timedelta, datetime
from config import Config
from news_sentiment_utils import save_news_sentiment_data_to_db, save_news_agg_to_db

# set global variables, parse parameters to url
max_news_items = 1000
time_from = (datetime.now() - timedelta(days=1)).strftime("%Y%m%dT%H%M")
url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&time_from={time_from}&limit={max_news_items}&apikey={Config.ALPHAVANTAGE_API_KEY}"

if __name__ == "__main__":
    save_news_sentiment_data_to_db(url, 300)
    save_news_agg_to_db()
