from datetime import datetime, timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from reddit_utils import (
    get_reddit_comments_to_rds,
    get_reddit_comments_raw_to_clean,
    get_reddit_comments_clean_to_emotion,
)


# Define Python functions for tasks
def task_get_comments_to_rds():
    return get_reddit_comments_to_rds("stock", post_limit=50, batch_size=300)


def task_raw_to_clean(**context):
    first_inserted_id = context["task_instance"].xcom_pull(
        task_ids="get_comments_to_rds_task"
    )
    return get_reddit_comments_raw_to_clean(first_inserted_id, batch_size=300)


def task_clean_to_emotion(**context):
    first_inserted_id = context["task_instance"].xcom_pull(task_ids="raw_to_clean_task")
    return get_reddit_comments_clean_to_emotion(
        first_inserted_id, batch_size_for_prediction=20, batch_size_for_insert=300
    )


# Define the default_args dictionary
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# define the dag
dag = DAG(
    "reddit_dag",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

# Define tasks
get_comments_to_rds_task = PythonOperator(
    task_id="get_comments_to_rds_task",
    python_callable=task_get_comments_to_rds,
    dag=dag,
)

raw_to_clean_task = PythonOperator(
    task_id="raw_to_clean_task",
    python_callable=task_raw_to_clean,
    provide_context=True,
    dag=dag,
)

clean_to_emotion_task = PythonOperator(
    task_id="clean_to_emotion_task",
    python_callable=task_clean_to_emotion,
    provide_context=True,
    dag=dag,
)

# Set up the order of the tasks
get_comments_to_rds_task >> raw_to_clean_task >> clean_to_emotion_task
