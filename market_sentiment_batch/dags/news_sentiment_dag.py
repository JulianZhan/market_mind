from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from airflow.operators.empty import EmptyOperator


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
    "news_sentiment_dag",
    default_args=default_args,
    schedule="0 0 * * *",
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

news_sentiment_task = EcsRunTaskOperator(
    task_id="news_sentiment_task",
    cluster="market-mind",
    task_definition="news-sentiment-task:2",
    launch_type="FARGATE",
    overrides={
        "executionRoleArn": "arn:aws:iam::145723653607:role/ecsTaskExecutionRole",
        "taskRoleArn": "arn:aws:iam::145723653607:role/ecsTaskExecutionRole",
    },
    network_configuration={
        "awsvpcConfiguration": {
            "subnets": "vpc-0fc70fccc5b9a1b95",
            "securityGroups": "sg-08d17d26eb8ea6c2e",
            "assignPublicIp": "ENABLED",
        },
    },
    awslogs_group="/ecs/news-sentiment-task",
    awslogs_region="ap-southeast-2",
    awslogs_stream_prefix="ecs",
    dag=dag,
)

# Set up the order of the tasks
(task_start >> news_sentiment_task >> task_finished)
