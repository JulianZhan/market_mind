import json
import pytest
from unittest.mock import ANY
from unittest.mock import patch, MagicMock
from market_trades_producer import (
    on_message,
    avro_encode,
    avro_schema,
    on_error,
    on_close,
    on_open,
    tickers,
)


# Mock WebSocketApp object
class MockWebSocketApp:
    def __init__(self):
        pass

    def close(self):
        pass

    def run_forever(self):
        pass

    def send(self, message):
        pass


def test_on_message_successful():
    # Mocking
    producer_mock = MagicMock()
    producer_mock.produce = MagicMock()

    # Sample data
    message_data = [{"ev": "XT", "x": 1}]

    with patch("market_trades_producer.producer", producer_mock):
        # Call on_message
        on_message(MockWebSocketApp(), json.dumps(message_data))

    # Validate
    producer_mock.produce.assert_called_once()
    producer_mock.produce.assert_called_with(
        topic=ANY, value=avro_encode({"data": message_data[0]}, avro_schema)
    )
    producer_mock.flush.assert_not_called()


def test_on_message_non_xt_message():
    # Mocking
    producer_mock = MagicMock()
    producer_mock.produce = MagicMock()
    producer_mock.flush = MagicMock()

    # Sample data
    message_data = [{"ev": "NonXT", "x": 1}]

    with patch("market_trades_producer.producer", producer_mock):
        # Call on_message
        on_message(MockWebSocketApp(), json.dumps(message_data))

    # Validate
    producer_mock.produce.assert_not_called()
    producer_mock.flush.assert_not_called()


def test_on_error():
    mock_ws = MockWebSocketApp()
    mock_ws.close = MagicMock()
    mock_ws.run_forever = MagicMock()

    on_error(mock_ws, "Sample error")

    mock_ws.close.assert_called_once()
    mock_ws.run_forever.assert_called_once()


def test_on_close():
    mock_ws = MockWebSocketApp()
    producer_mock = MagicMock()
    producer_mock.flush = MagicMock()

    with patch("market_trades_producer.producer", producer_mock):
        on_close(mock_ws, 500, "Sample reason")

    producer_mock.flush.assert_called_once()


def test_on_open():
    mock_ws = MockWebSocketApp()
    mock_ws.send = MagicMock()

    on_open(mock_ws)

    assert mock_ws.send.call_count == 2

    mock_ws.send.assert_any_call(json.dumps({"action": "subscribe", "params": tickers}))
