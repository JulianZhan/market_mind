import pytest
from unittest.mock import patch, Mock
from api_utils import (
    validate_date,
    score_definition,
    get_news_sentiment,
    get_reddit_emotion,
)


def test_validate_correct_date():
    """
    test validate_date function with correct date
    """
    correct_date1 = "2021-01-01"
    correct_date2 = "2021-01-31"
    correct_date3 = "2021-12-31"

    validate_date(correct_date1)
    validate_date(correct_date2)
    validate_date(correct_date3)


def test_validate_wrong_date():
    """
    test validate_date function with wrong date
    which should raise ValueError
    """
    wrong_date1 = "2021-01-0"
    wrong_date2 = "2021-01-0a"
    wrong_date3 = "2021-01-0-"
    wrong_date4 = "abc"
    wrong_date5 = ""

    with pytest.raises(ValueError):
        validate_date(wrong_date1)
    with pytest.raises(ValueError):
        validate_date(wrong_date2)
    with pytest.raises(ValueError):
        validate_date(wrong_date3)
    with pytest.raises(ValueError):
        validate_date(wrong_date4)
    with pytest.raises(ValueError):
        validate_date(wrong_date5)


@pytest.fixture
def mock_session_fixture():
    """
    set up and return a mock session
    fixture use dependency injection to inject the mock session
    for other test functions that use the same name as the {mock_session_fixture}
    pytest will automatically inject the mock session

    Returns:
        Mock: mock session
    """
    session = Mock()
    return session


# using patch decorator to specify that Seesion object should be patched with mock_session_fixture in the test function
@patch("api_utils.Session")
def test_get_news_sentiment(mock_session_fixture):
    """
    test get_news_sentiment function to check if the function returns the correct result and format

    Args:
        mock_session_fixture (Mock): mock session, mock_session_fixture is a fixture and will be injected by pytest
    """

    # mock_session_fixture is a fixture and will be injected by pytest
    # return_value is Mock() object, __enter__ is a magic method that used for context manager
    # the return value of __enter__ is also a Mock() object
    mock_session = mock_session_fixture.return_value.__enter__.return_value
    mock_news_sentiment = Mock()
    mock_news_sentiment.avg_score = 0.5
    mock_news_sentiment.max_score = 1.0
    mock_news_sentiment.min_score = 0.0
    mock_news_sentiment.std_score = 0.2
    mock_session.query().filter().first.return_value = mock_news_sentiment

    result = get_news_sentiment("2022-01-20")

    assert result == {
        "score_definition": score_definition,
        "score": {
            "avg_score": 0.5,
            "max_score": 1.0,
            "min_score": 0.0,
            "std_score": 0.2,
        },
        "date_recorded": "2022-01-20",
    }


# using patch decorator to specify that Seesion object should be patched with mock_session_fixture in the test function
@patch("api_utils.Session")
def test_get_reddit_emotion(mock_session_fixture):
    """
    test get_news_sentiment function to check if the function returns the correct result and format

    Args:
        mock_session_fixture (Mock): mock session, mock_session_fixture is a fixture and will be injected by pytest
    """
    mock_session = mock_session_fixture.return_value.__enter__.return_value
    mock_reddit_emotion_1 = Mock()
    mock_reddit_emotion_1.emotion_name = "Happy"
    mock_reddit_emotion_1.avg_score = 0.5

    mock_reddit_emotion_2 = Mock()
    mock_reddit_emotion_2.emotion_name = "Sad"
    mock_reddit_emotion_2.avg_score = -0.5

    mock_session.query().filter().all.return_value = [
        mock_reddit_emotion_1,
        mock_reddit_emotion_2,
    ]

    result = get_reddit_emotion("2022-01-20")

    assert result == {
        "emotion": {"Happy": 0.5, "Sad": -0.5},
        "date_recorded": "2022-01-20",
    }
