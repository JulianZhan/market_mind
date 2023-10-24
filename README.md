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

How Market Mind reaches its users:

**Request Routing**: User requests, initiated via URL, hit Route 53 (DNS service) first. Based on subdomains, Route 53 routes the requests:

 - Web Frontend: To CloudFront (CDN) which sits in front of S3.
 - API, Grafana, Airflow, Backend: To Application Load Balancer, which subsequently routes them to specific ECS Fargate servers.

**Auto-scaling**: To manage demand efficiently, the Auto Scaling Group scales the number of servers based on API and Backend CPU utilization.

### Servers Monitoring Architecture
![Servers Monitoring Architecture](https://github.com/JulianZhan/market_mind/raw/refactoring/project_architecture/servers_monitoring_architecture.jpg)

### Airflow Batch Pipelines Architecture
![Airflow Batch Pipelines Architecture](https://github.com/JulianZhan/market_mind/raw/refactoring/project_architecture/airflow_batch_pipelines_architecture.jpg)
