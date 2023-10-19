import pytest
from unittest.mock import patch, MagicMock, ANY
import json
from market_trades_producer import (
    on_message,
    avro_encode,
    on_error,
    on_close,
    on_open,
    tickers,
    avro_schema,
)


def test_on_message_successful():
    """
    test on_message function with a valid message
    """
    mock_ws = MagicMock()
    mock_producer = MagicMock()
    mock_producer.produce = MagicMock()
    mock_producer.flush = MagicMock()
    message_data = [{"ev": "XT", "x": 1}]

    # replace producer with mock_producer
    with patch("market_trades_producer.producer", mock_producer):
        on_message(mock_ws, json.dumps(message_data))

    mock_producer.produce.assert_called_once()
    # assert that produce is called with the correct arguments
    mock_producer.produce.assert_called_with(
        topic=ANY, value=avro_encode({"data": message_data[0]}, avro_schema)
    )
    mock_producer.flush.assert_not_called()


def test_on_message_non_xt_message():
    """
    test on_message function with a non XT message
    """
    mock_ws = MagicMock()
    mock_producer = MagicMock()
    mock_producer.produce = MagicMock()
    mock_producer.flush = MagicMock()
    message_data = [{"ev": "NonXT", "x": 1}]

    # replace producer with mock_producer
    with patch("market_trades_producer.producer", mock_producer):
        on_message(mock_ws, json.dumps(message_data))

    mock_producer.produce.assert_not_called()
    mock_producer.flush.assert_not_called()


def test_on_error():
    """
    test situation where on_error os callend and run_forever should be triggered to retry connection
    """
    mock_ws = MagicMock()
    mock_ws.close = MagicMock()
    mock_ws.run_forever = MagicMock()

    on_error(mock_ws, "Sample error")

    mock_ws.close.assert_called_once()
    mock_ws.run_forever.assert_called_once()


def test_on_close():
    """
    test situation where on_close is called and producer should implement flush
    """
    mock_ws = MagicMock()
    mock_producer = MagicMock()
    mock_producer.flush = MagicMock()

    # replace producer with mock_producer
    with patch("market_trades_producer.producer", mock_producer):
        on_close(mock_ws, 500, "Sample reason")

    mock_producer.flush.assert_called_once()


def test_on_open():
    """
    test situation where on_open is called
    and websocket should send subscribe message and auth message
    """
    mock_ws = MagicMock()
    mock_ws.send = MagicMock()

    on_open(mock_ws)

    assert mock_ws.send.call_count == 2
    mock_ws.send.assert_any_call(json.dumps({"action": "subscribe", "params": tickers}))
