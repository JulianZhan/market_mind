from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, explode, current_timestamp, concat_ws
from pyspark.sql.avro.functions import from_avro
import sys

sys.path.append("../")
from config import Config
import os

# setting required packages for pysaprk and kafka integration
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/java/"
SPARK_VERSION = "3.4.1"
os.environ["PYSPARK_SUBMIT_ARGS"] = (
    f"--jars ./mysql-connector-java-8.0.26.jar "
    f"--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:{SPARK_VERSION},"
    f"org.apache.spark:spark-sql-kafka-0-10_2.12:{SPARK_VERSION},"
    f"org.apache.spark:spark-avro_2.12:{SPARK_VERSION} "
    f"pyspark-shell"
)


spark = SparkSession.builder.appName("trades_consumer").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
# topic name rule: topic_prefix.schema.table
kafka_topic_name = f"{Config.KAFKA_TOPIC_NAME}"
kafka_bootstrap_server = f"{Config.KAFAK_SERVER}:{Config.KAFKA_PORT}"
batch_size = "100"
trades_schema = open("trades_schema.avsc", "r").read()
jdbc_url = f"jdbc:mysql://{Config.RDS_HOSTNAME}:{Config.RDS_PORT}/{Config.RDS_DB_NAME}"
raw_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", kafka_bootstrap_server)
    .option("subscribe", kafka_topic_name)
    .option("startingOffsets", "earliest")
    .option("maxOffsetsPerTrigger", batch_size)
    .load()
)


# Explode the data from Avro
decoded_df = (
    raw_df.withColumn("avro_data", from_avro(col("value"), trades_schema))
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
    .withColumn("trade_conditions", concat_ws(",", col("trade_conditions")))
)


def insert_to_rds(batch_df, batch_id):
    batch_df.write.jdbc(
        url=jdbc_url,
        table="trades",
        mode="append",
        properties={
            "user": Config.RDS_USER,
            "password": Config.RDS_PASSWORD,
            "driver": "com.mysql.cj.jdbc.Driver",
        },
    )


query = final_df.writeStream.outputMode("append").foreachBatch(insert_to_rds).start()
query.awaitTermination()
