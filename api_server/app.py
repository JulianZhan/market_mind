from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class MarketSentiment(Resource):
    def get(self):
        return {"hello": "world"}
