from utils import avro_encode
import avro.schema
import pytest


def test_avro_encode():
    # Define schema
    schema = avro.schema.parse(open("trades_schema.avsc").read())

    # Define data matching the schema
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

    # Call avro_encode
    result = avro_encode(data, schema)

    # Assert result is bytes
    assert isinstance(result, bytes)


def test_encoding_with_incorrect_data_type():
    schema = avro.schema.parse(open("trades_schema.avsc").read())
    # Define data matching the schema
    data = {
        "data": {
            "c": "should be a list",
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
    with pytest.raises(Exception):
        avro_encode(data, schema)
