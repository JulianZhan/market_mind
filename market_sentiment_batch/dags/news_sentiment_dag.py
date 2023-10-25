from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from airflow.operators.empty import EmptyOperator


# define the default_args dictionary for dag
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

# trigger the ECS task to actually run the data pipeline
news_sentiment_task = EcsRunTaskOperator(
    task_id="news_sentiment_task",
    cluster="market-mind",
    task_definition="news-sentiment-task:2",
    launch_type="FARGATE",
    region="ap-southeast-2",
    overrides={
        "executionRoleArn": "arn:aws:iam::145723653607:role/ecsTaskExecutionRole",
        "taskRoleArn": "arn:aws:iam::145723653607:role/ecsTaskExecutionRole",
    },
    network_configuration={
        "awsvpcConfiguration": {
            "securityGroups": ["sg-08d17d26eb8ea6c2e"],
            "subnets": [
                "subnet-0cf71e0cf5d773ad4",
                "subnet-0f6b1c2ca448ec20f",
                "subnet-02b7717f0ab78def5",
            ],
            "assignPublicIp": "ENABLED",
        },
    },
    dag=dag,
)

# set up the order of the tasks
(task_start >> news_sentiment_task >> task_finished)
