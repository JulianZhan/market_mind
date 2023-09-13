from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, explode, current_timestamp, avg
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.streaming import Trigger
from config import Config
import os

# setting required packages for pysaprk and kafka integration
os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.4.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1"


park = SparkSession.builder.appName("Kafka_cdc").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
# topic name rule: topic_prefix.schema.table
KAFKA_TOPIC_NAME = f"{Config.KAFKA_TOPIC_NAME}"
KAFKA_BOOTSTRAP_SERVER = f"{Config.KAFAK_SERVER}:{Config.KAFKA_PORT}"
BATCH_SIZE = "100"
TRADES_SCHEMA = open("trades_schema.avsc", "r").read()
raw_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)
    .option("subscribe", KAFKA_TOPIC_NAME)
    .option("startingOffsets", "earliest")
    .option("maxOffsetsPerTrigger", BATCH_SIZE)
    .load()
)


# Explode the data from Avro
decoded_df = (
    raw_df.withColumn("avro_data", from_avro(col("value"), TRADES_SCHEMA))
    .select("avro_data.*")
    .select(explode(col("data")), col("type"))
    .select("col.*")
)

# Rename columns and add proper timestamps
final_df = (
    decoded_df.withColumnRenamed("c", "trade_conditions")
    .withColumnRenamed("p", "price")
    .withColumnRenamed("s", "symbol")
    .withColumnRenamed("t", "trade_timestamp")
    .withColumnRenamed("v", "volume")
    .withColumn("trade_timestamp", (col("trade_timestamp") / 1000).cast("timestamp"))
    .withColumn("created_at", current_timestamp())
)
