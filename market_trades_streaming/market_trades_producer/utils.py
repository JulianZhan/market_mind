import io
import avro.schema
import avro.io


# encode message into avro format
def avro_encode(data: dict, schema) -> bytes:
    """
    encode message into avro format

    Args:
        data (dict): message to encode
        schema (Union[avro.schema.Schema, avro.schema.RecordSchema]): avro schema

    Returns:
        bytes: encoded message
    """
    # specify schema
    writer = avro.io.DatumWriter(schema)
    # initialize bytes writer
    bytes_writer = io.BytesIO()
    # initialize encoder
    encoder = avro.io.BinaryEncoder(bytes_writer)
    # write data
    writer.write(data, encoder)
    return bytes_writer.getvalue()
