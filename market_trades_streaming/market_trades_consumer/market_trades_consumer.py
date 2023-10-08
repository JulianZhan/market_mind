from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, current_timestamp, concat_ws
from pyspark.sql.avro.functions import from_avro
import pyspark.sql.dataframe
import logging
from config import Config
from typing import Optional
from prometheus_client import start_http_server, Counter, Summary

# Metrics

decode_time: Summary = Summary(
    "pyspark_consumer_decode_time_seconds", "Time spent decoding a batch"
)
parse_time: Summary = Summary(
    "pyspark_consumer_parse_time_seconds", "Time spent parsing a batch"
)
insert_time: Summary = Summary(
    "pyspark_consumer_insert_time_seconds", "Time spent inserting a batch"
)
decode_errors: Summary = Counter(
    "pyspark_consumer_decode_errors", "Errors encountered while decoding Avro"
)
parse_errors: Summary = Counter(
    "pyspark_consumer_parse_errors", "Errors encountered while parsing"
)
database_errors: Summary = Counter(
    "pyspark_consumer_database_errors", "Errors encountered while inserting into RDS"
)


@decode_time.time()
def decode_avro_df(
    raw_df: pyspark.sql.dataframe.DataFrame, trades_schema: str
) -> Optional[pyspark.sql.dataframe.DataFrame]:
    """
    decode avro data from kafka

    Args:
        raw_df (pyspark.sql.dataframe.DataFrame): raw dataframe from kafka
        trades_schema (str): avro schema

    Returns:
        pyspark.sql.dataframe.DataFrame: decoded dataframe
    """
    try:
        decoded_df: pyspark.sql.dataframe.DataFrame = (
            raw_df.withColumn("avro_data", from_avro(col("value"), trades_schema))
            .select("avro_data.*")
            .select(explode(col("data")), col("type"))
            .select("col.*")
        )
        return decoded_df
    except Exception as e:
        logger.error(f"Failed to decode Avro: {e}, raw_df: {raw_df}")
        decode_errors.inc()


@parse_time.time()
def parse_decoded_df(
    decoded_df: pyspark.sql.dataframe.DataFrame,
) -> Optional[pyspark.sql.dataframe.DataFrame]:
    """
    parse decoded dataframe, with columns renamed and timestamp converted to datetime

    Args:
        decoded_df (pyspark.sql.dataframe.DataFrame): decoded dataframe

    Returns:
        pyspark.sql.dataframe.DataFrame: parsed dataframe
    """
    try:
        final_df: pyspark.sql.dataframe.DataFrame = (
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
    except Exception as e:
        logger.error(
            f"Failed to parse decoded dataframe: {e}, decoded_df: {decoded_df}"
        )
        parse_errors.inc()


@insert_time.time()
def insert_to_rds(batch_df: pyspark.sql.dataframe.DataFrame, batch_id: int) -> None:
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
        database_errors.inc()


if __name__ == "__main__":
    start_http_server(5052)

    # set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logger: logging.Logger = logging.getLogger(__name__)

    # define spark session
    spark: SparkSession = (
        SparkSession.builder.appName("trades_consumer").master("local[*]").getOrCreate()
    )
    # set log level
    spark.sparkContext.setLogLevel("ERROR")
    # define kafka and mysql connection details
    kafka_topic_name: str = f"{Config.KAFKA_TOPIC_NAME}"
    kafka_bootstrap_server: str = f"{Config.KAFAK_SERVER}:{Config.KAFKA_PORT}"
    batch_size: str = "3000"
    trades_schema: str = open("trades_schema.avsc", "r").read()
    jdbc_url: str = (
        f"jdbc:mysql://{Config.RDS_HOSTNAME}:{Config.RDS_PORT}/{Config.RDS_DB_NAME}"
    )

    # read streaming data from kafka
    raw_df: pyspark.sql.dataframe.DataFrame = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap_server)
        .option("subscribe", kafka_topic_name)
        .option("startingOffsets", "latest")
        .option("maxOffsetsPerTrigger", batch_size)
        .load()
    )

    # decode the avro data
    decoded_df: Optional[pyspark.sql.dataframe.DataFrame] = decode_avro_df(
        raw_df, trades_schema
    )
    # parse the decoded data
    if isinstance(decoded_df, pyspark.sql.dataframe.DataFrame):
        final_df: Optional[pyspark.sql.dataframe.DataFrame] = parse_decoded_df(
            decoded_df
        )
        if isinstance(final_df, pyspark.sql.dataframe.DataFrame):
            # write to RDS, with batch insert
            query = final_df.writeStream.foreachBatch(insert_to_rds).start()
            query.awaitTermination()
