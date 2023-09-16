from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from config import Config
from news_sentiment_utils import save_news_sentiment_data_to_db, save_news_agg_to_db

# set global variables, parse parameters to url
max_news_items = 1000
time_from = (datetime.now() - timedelta(days=1)).strftime("%Y%m%dT%H%M")
url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&time_from={time_from}&limit={max_news_items}&apikey={Config.ALPHAVANTAGE_API_KEY}"


# default arguments for airflow dag
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

# define the dag
dag = DAG(
    "news_sentiment_dag",
    default_args=default_args,
    schedule=timedelta(days=1),
    catchup=False,
)

task_start = EmptyOperator(
    task_id="task_start",
    dag=dag,
)

task_finished = EmptyOperator(
    task_id="task_finished",
    dag=dag,
)


# define the tasks, use op_args to pass arguments to python callable function
get_news_sentiment_data_task = PythonOperator(
    task_id="get_news_sentiment_data",
    python_callable=save_news_sentiment_data_to_db,
    op_args=[url, 300],
    dag=dag,
)

get_news_agg_task = PythonOperator(
    task_id="get_news_agg", python_callable=save_news_agg_to_db, dag=dag
)

# define the task dependencies
task_start >> get_news_sentiment_data_task >> get_news_agg_task >> task_finished
