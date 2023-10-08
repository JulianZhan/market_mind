FROM bitnami/spark:3.4.1

# set the working directory in the container
WORKDIR /app

# copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r requirements.txt

# install required pyspark packages for mysql connector and kafka connector
ENV SPARK_VERSION=3.4.1
ENV PYSPARK_SUBMIT_ARGS="--jars ./mysql-connector-java-8.0.26.jar --packages org.apache.spark:spark-streaming-kafka-0-10_2.12:${SPARK_VERSION},org.apache.spark:spark-sql-kafka-0-10_2.12:${SPARK_VERSION},org.apache.spark:spark-avro_2.12:${SPARK_VERSION} pyspark-shell"

# run python script when the container launches
CMD ["python", "market_trades_consumer.py"]
