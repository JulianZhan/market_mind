# Dockerfile
FROM apache/airflow:2.7.1

# Create cache directory for transformers and set permissions
RUN mkdir -p /tmp/transformers_cache && chmod 777 /tmp/transformers_cache

# Create the environment
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --upgrade praw

CMD ["python", "dags/reddit_utils.py"]