from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago
from config import Config

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "news_sentiment_dag",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

task_start = DummyOperator(
    task_id="task_start",
    dag=dag,
)

task_finished = DummyOperator(
    task_id="task_finished",
    dag=dag,
)


data_migration_task = PythonOperator(
    task_id="data_migration_task", python_callable=migrate_gov_to_gcs, dag=dag
)

task_start >> data_migration_task >> task_finished
