# Market Mind
Market Mind provides a comprehensive solution for investors by offering latest market sentiment, emotion analysis, and real-time BTC price streaming.

## Features:
**Real-time BTC Price** Streaming from Polygon.io API. \
**Market Sentiment Analysis** from Alpha Vantage API. \
**Market Emotion Analysis** by crawling Reddit comments in the CryptoCurrency subreddit using PRAW, and processing with LLM. 



## Architecture
### Overall Architecture
![Overall Architecture](https://github.com/JulianZhan/market_mind/raw/refactoring/project_architecture/overall_architecture.jpg)

Here's a brief overview of Market Mind's architecture:

**Containerization**: All services are packaged within Docker containers, mainly managed and deployed via AWS ECS and Fargate.

**Market Trades**: Polygon.io API streams BTC price data. This data is collected by a Python producer, sent to Kafka, processed by PySpark Structured Streaming, and finally stored in RDS MySQL.


**Market Sentiment & Emotion**: 
 - Workflow: Alpha Vantage API provides financial news and market sentiment. Reddit comments, collected through PRAW, implement emotion analysis using LLM. Both are stored in RDS MySQL.
 - Data Orchestration: Airflow, hosted on an EC2 instance with docker-compose, orchestrates batch pipelines and triggers tasks to run. Airflow serves as pure orchestrator, actual computations are executed by ECS Fargate tasks. Moreover, LLM is deployed on SageMaker for serverless inference.

**Database**: RDS MySQL offers data consistency and cost-effectiveness, and is set up for scalability.

**API Server**: Flask serves data from RDS MySQL and listens to Kafka for real-time trades to users. It uses WebSocket to provide users with live trade streams. This API aims to provide a easy-to-use connection point for users.

**Web Backend**: Developed using Spring Boot in Java. Spring Data JPA facilitates RDS MySQL connectivity. Java is chosen for its statical typing and strong type checking, which helps to avoid bugs and improve code quality for a large codebase.

**Web Frontend**: React offers an interactive and visually appealing user interface.

### Content Delivery Architecture
![Content Delivery Architecture](https://github.com/JulianZhan/market_mind/raw/refactoring/project_architecture/content_delivery_architecture.jpg)

How Market Mind delivers content to users:

**Request Routing**: User send requests via URL, hit Route 53 (DNS service) first. Based on subdomains, Route 53 routes the requests:

 - Web Frontend: To CloudFront (CDN) which sits in front of S3.
 - API, Grafana, Airflow, Backend: To Application Load Balancer, which subsequently routes them to target ECS Fargate servers.

**Auto-scaling**: To manage demand from clients efficiently, the Auto Scaling Group scales the number of servers based on API and Backend CPU utilization.

### Servers Monitoring Architecture
![Servers Monitoring Architecture](https://github.com/JulianZhan/market_mind/raw/refactoring/project_architecture/servers_monitoring_architecture.jpg)

Market Mind employs Cloud Map to efficiently monitor its server operations.

**How it Works**: 

 - Prometheus Integration: \
Role of Cloud Map: Cloud Map registers servers and provides DNS, enabling Prometheus to locate them. \
Metrics Collection: Prometheus periodically fetches **user-defined metrics** from these servers and retains them in its database. \
Visualization: Grafana collects these metrics from Prometheus and provides a visual representation. 

 - CloudWatch Integration: \
Monitoring: CloudWatch **tracks logs and infrastructure-related metrics** from servers.
Visualization: Grafana retrieves logs and metrics from CloudWatch to provide a visual analysis.


### Airflow Batch Pipelines Architecture
![Airflow Batch Pipelines Architecture](https://github.com/JulianZhan/market_mind/raw/refactoring/project_architecture/airflow_batch_pipelines_architecture.jpg)

For efficient operation of batch data pipelines, Airflow operates as the primary orchestrator. And ECS Fargate tasks serve as the computational engines. Then, SageMaker endpoints are activated for serverless inference. This architecture is designed to be scalable and cost-effective.

**How it Works**:
 - Task Scheduling: Airflow sets up tasks to be executed on a scheduled basis.

 - Data Computation: Once scheduled, Airflow signals ECS Fargate tasks, which function as the computational engines and run.

 - Sentiment & Emotion Analysis: For sentiment and emotion analyses, the ECS Fargate tasks activate SageMaker endpoints to execute the inference.

## Deployment
Airflow is deployed on an EC2 instance with docker-compose. \
All other services are deployed on AWS ECS Fargate with provided task definitions and service definitions. \
All services are containerized with Docker.

### Airflow   
 - Install docker-compose on EC2 instance.
 - Clone this repo.
 - Run `docker-compose up` in the market_sentiment_backend folder.

### Airflow Tasks
 Create a task definition for each service, using the provided task definitions. Execute the following commands in aws-cli to register reddit task and news sentiment task: 
```
aws ecs register-task-definition \
--cli-input-json file://task-definition.json
```

### All Other Services
 - Create a cluster, called `market-mind`
 - Create a task definition for each service, using the provided task definitions. Execute the following commands in aws-cli to register each task:
 ```
aws ecs register-task-definition \
--cli-input-json file://task-definition.json
```
 - Execute the following commands in aws-cli to create a service for each task:
 ```
 aws ecs create-service \
      --cli-input-json file://ecs-service-registry.json
```

The rest of the services are deployed in the same way. \
Moreover, the required permissions should be granted to the task roles and users.
