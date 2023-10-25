from utils import avro_encode
import avro.schema
import pytest


def test_avro_encode():
    """
    test if avro_encode returns bytes when given a valid schema and data
    """
    schema = avro.schema.parse(open("trades_schema.avsc").read())
    data = {
        "data": {
            "c": [1],
            "ev": "SampleEvent",
            "i": "SampleTradeID",
            "p": 123.45,
            "pair": "BTC-USD",
            "r": 11111111,
            "s": 0.1234,
            "t": 11111111,
            "x": 1,
        }
    }

    result = avro_encode(data, schema)

    assert isinstance(result, bytes)


def test_encoding_with_incorrect_data_type():
    """
    test if avro_encode raises an exception when given an invalid schema and data
    """
    schema = avro.schema.parse(open("trades_schema.avsc").read())
    data = {
        "data": {
            "c": "should be a list",  # should be a list, not a string
            "ev": "SampleEvent",
            "i": "SampleTradeID",
            "p": 123.45,
            "pair": "BTC-USD",
            "r": 11111111,
            "s": 0.1234,
            "t": 11111111,
            "x": 1,
        }
    }

    # assert that an exception is raised
    with pytest.raises(Exception):
        avro_encode(data, schema)
