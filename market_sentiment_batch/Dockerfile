# Dockerfile
FROM apache/airflow:2.7.1

# Create the environment
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --upgrade praw

CMD ["python", "dags/reddit_utils.py"]