import pytest
from unittest.mock import Mock, patch
from news_sentiment_utils import (
    get_news_sentiment_data,
)


def test_get_news_sentiment_data_successful_response():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"feed": [{"key": "value"}], "items": 1}
    with patch("requests.get", return_value=mock_response):
        result = get_news_sentiment_data("http://example.com")
        assert result == [{"key": "value"}]


def test_get_news_sentiment_data_no_items():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": 0}
    with patch("requests.get", return_value=mock_response):
        result = get_news_sentiment_data("http://example.com")
        assert result is None


def test_get_news_sentiment_data_error_response():
    mock_response = Mock()
    mock_response.status_code = 400
    with patch("requests.get", return_value=mock_response):
        result = get_news_sentiment_data("http://example.com")
        assert result is None
