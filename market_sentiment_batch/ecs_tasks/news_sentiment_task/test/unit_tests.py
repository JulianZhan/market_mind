import pytest
from unittest.mock import Mock, patch
from news_sentiment_utils import (
    get_news_sentiment_data,
)


def test_get_news_sentiment_data_successful_response():
    """
    test if get_news_sentiment_data function returns news sentiment data
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"feed": [{"key": "value"}], "items": 1}

    # use patch to mock requests.get with mock_response
    with patch("requests.get", return_value=mock_response):
        result = get_news_sentiment_data("http://example.com")
        assert result == [{"key": "value"}]


def test_get_news_sentiment_data_no_items():
    """
    test if get_news_sentiment_data function returns None when no news items found
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": 0}
    # use patch to mock requests.get with mock_response
    with patch("requests.get", return_value=mock_response):
        result = get_news_sentiment_data("http://example.com")
        assert result is None


def test_get_news_sentiment_data_error_response():
    """
    test if get_news_sentiment_data function returns None when error response
    """
    mock_response = Mock()
    mock_response.status_code = 400
    # use patch to mock requests.get with mock_response
    with patch("requests.get", return_value=mock_response):
        result = get_news_sentiment_data("http://example.com")
        assert result is None
