from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sentiment_model import AlphaVantageAgg, RedditAgg
from api_utils import get_news_sentiment, get_reddit_emotion, validate_date

app = Flask(__name__)
api = Api(app)


class MarketSentiment(Resource):
    def get(self):
        target_date = request.args.get("date")
        try:
            validate_date(target_date)
        except ValueError as e:
            return jsonify({"message": "invalid date, please use YYYY-MM-DD format"})
        news_sentiment = get_news_sentiment(target_date)
        return jsonify({"message": "success", "data": news_sentiment})


class MarketEmotion(Resource):
    def get(self):
        target_date = request.args.get("date")
        try:
            validate_date(target_date)
        except ValueError as e:
            return jsonify({"message": "invalid date, please use YYYY-MM-DD format"})
        reddit_emotion = get_reddit_emotion(target_date)
        return jsonify({"message": "success", "data": reddit_emotion})


api.add_resource(MarketSentiment, "/market_sentiment")
api.add_resource(MarketEmotion, "/market_emotion")
