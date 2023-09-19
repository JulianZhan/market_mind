FROM bitnami/spark:3.4.1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r requirements.txt

# Install required packages for mysql connector and kafka connector
ENV SPARK_VERSION=3.4.1
ENV PYSPARK_SUBMIT_ARGS="--jars ./mysql-connector-java-8.0.26.jar --packages org.apache.spark:spark-streaming-kafka-0-10_2.12:${SPARK_VERSION},org.apache.spark:spark-sql-kafka-0-10_2.12:${SPARK_VERSION},org.apache.spark:spark-avro_2.12:${SPARK_VERSION} pyspark-shell"

# Run your script when the container launches
CMD ["python", "market_trades_consumer.py"]
