from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from reddit_utils import (
    get_reddit_comments_to_rds,
    get_reddit_comments_raw_to_clean,
    get_reddit_comments_clean_to_emotion,
    get_reddit_agg_to_db,
)


# Define Python functions for tasks
def task_get_comments_to_rds():
    return get_reddit_comments_to_rds("stock", post_limit=50, batch_size=300)


def task_raw_to_clean(**context):
    first_inserted_at = context["task_instance"].xcom_pull(
        task_ids="get_comments_to_rds_task"
    )
    return get_reddit_comments_raw_to_clean(first_inserted_at, batch_size=300)


def task_clean_to_emotion(**context):
    first_inserted_at = context["task_instance"].xcom_pull(task_ids="raw_to_clean_task")
    return get_reddit_comments_clean_to_emotion(
        first_inserted_at, batch_size_for_prediction=20, batch_size_for_insert=300
    )


# Define the default_args dictionary
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
    "reddit_dag",
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


# Define tasks
get_comments_to_rds_task = PythonOperator(
    task_id="get_comments_to_rds_task",
    python_callable=task_get_comments_to_rds,
    dag=dag,
)

raw_to_clean_task = PythonOperator(
    task_id="raw_to_clean_task",
    python_callable=task_raw_to_clean,
    dag=dag,
)

clean_to_emotion_task = PythonOperator(
    task_id="clean_to_emotion_task",
    python_callable=task_clean_to_emotion,
    dag=dag,
)

get_reddit_agg_task = PythonOperator(
    task_id="get_reddit_agg", python_callable=get_reddit_agg_to_db, dag=dag
)

# Set up the order of the tasks
(
    task_start
    >> get_comments_to_rds_task
    >> raw_to_clean_task
    >> clean_to_emotion_task
    >> get_reddit_agg_task
    >> task_finished
)
