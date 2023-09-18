from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, current_timestamp, concat_ws
from pyspark.sql.avro.functions import from_avro
import logging
from config import Config


def decode_avro_df(raw_df, trades_schema):
    """
    decode avro data from kafka

    Args:
        raw_df (pyspark.sql.dataframe.DataFrame): raw dataframe from kafka
        trades_schema (avro.schema): avro schema

    Returns:
        pyspark.sql.dataframe.DataFrame: decoded dataframe
    """
    decoded_df = (
        raw_df.withColumn("avro_data", from_avro(col("value"), trades_schema))
        .select("avro_data.*")
        .select(explode(col("data")), col("type"))
        .select("col.*")
    )
    return decoded_df


def parse_decoded_df(decoded_df):
    """
    parse decoded dataframe, with columns renamed and timestamp converted to datetime

    Args:
        decoded_df (pyspark.sql.dataframe.DataFrame): decoded dataframe

    Returns:
        pyspark.sql.dataframe.DataFrame: parsed dataframe
    """
    final_df = (
        decoded_df.withColumnRenamed("c", "trade_conditions")
        .withColumnRenamed("p", "price")
        .withColumnRenamed("s", "symbol")
        .withColumnRenamed("t", "trade_timestamp")
        .withColumnRenamed("v", "volume")
        .withColumn(
            "trade_timestamp", (col("trade_timestamp") / 1000).cast("timestamp")
        )
        .withColumn("created_at", current_timestamp())
        .withColumn("trade_conditions", concat_ws(",", col("trade_conditions")))
    )
    return final_df


def insert_to_rds(batch_df, batch_id):
    """
    batch insert to RDS from pyspark dataframe

    Args:
        batch_df (pyspark.sql.dataframe.DataFrame): dataframe to insert
        batch_id (int): batch id
    """
    try:
        batch_df.write.format("jdbc").options(
            url=jdbc_url,
            driver="com.mysql.cj.jdbc.Driver",
            dbtable="trades",
            user=Config.RDS_USER,
            password=Config.RDS_PASSWORD,
            isolationLevel="NONE",
        ).mode("append").save()
    except Exception as e:
        logger.error(
            f"Failed to insert to RDS: {e}, batch_id: {batch_id}, batch_df: {batch_df}"
        )


if __name__ == "__main__":
    # set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logger = logging.getLogger(__name__)

    # define spark session
    spark = (
        SparkSession.builder.appName("trades_consumer").master("local[*]").getOrCreate()
    )
    # set log level
    spark.sparkContext.setLogLevel("ERROR")
    # define kafka and mysql connection details
    kafka_topic_name = f"{Config.KAFKA_TOPIC_NAME}"
    kafka_bootstrap_server = f"{Config.KAFAK_SERVER}:{Config.KAFKA_PORT}"
    batch_size = "1000"
    trades_schema = open("trades_schema.avsc", "r").read()
    jdbc_url = (
        f"jdbc:mysql://{Config.RDS_HOSTNAME}:{Config.RDS_PORT}/{Config.RDS_DB_NAME}"
    )

    # read streaming data from kafka
    raw_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap_server)
        .option("subscribe", kafka_topic_name)
        .option("startingOffsets", "latest")
        .option("maxOffsetsPerTrigger", batch_size)
        .load()
    )

    # decode the avro data
    try:
        decoded_df = decode_avro_df(raw_df, trades_schema)
    except Exception as e:
        logger.error(f"Failed to decode Avro: {e}, raw_df: {raw_df}")
    # parse the decoded data
    try:
        final_df = parse_decoded_df(decoded_df)
    except Exception as e:
        logger.error(f"Failed to parse decoded df: {e}, decoded_df: {decoded_df}")

    # write to RDS, with batch insert
    query = final_df.writeStream.foreachBatch(insert_to_rds).start()
    query.awaitTermination()
