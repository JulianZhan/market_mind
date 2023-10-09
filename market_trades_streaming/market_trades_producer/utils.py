import io
import avro.schema
import avro.io


# validate if ticker exists in finnhub
def ticker_validator(finnhub_client, ticker: str) -> bool:
    """
    check if ticker exists in finnhub

    Args:
        finnhub_client (finnhub.Client): finnhub client
        ticker (str): ticker to validate

    Returns:
        bool: True if ticker exists, False otherwise
    """
    for stock in finnhub_client.symbol_lookup(ticker)["result"]:
        if stock["symbol"] == ticker:
            return True
    return False


# encode message into avro format
def avro_encode(data: dict, schema) -> bytes:
    """
    encode message into predefined avro schema

    Args:
        data (dict): message to encode
        schema (avro.schema): avro schema

    Returns:
        bytes: encoded message
    """

    # specify avro schema
    writer = avro.io.DatumWriter(schema)
    # initialize bytes writer
    bytes_writer = io.BytesIO()
    # initialize avro encoder
    encoder = avro.io.BinaryEncoder(bytes_writer)
    # write data
    writer.write(data, encoder)
    return bytes_writer.getvalue()
