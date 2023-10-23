# Market Mind
Market Mind dedicates to provide latest market sentiment and emotion analysis, with realtime streaming BTC price, for users to make better investment decisions.
Market Mind collects data from Alpha Vantage API for financial news and news sentiment analysis. For market emotion, PRAW is used for crawling Reddit comments at CryptoCurrency subreddit, and LLM is utilized for market emotion analysis. Moreover, Market Mind provides realtime streaming BTC price from Polygon.io API.



## Architecture
![Overall Architecture](https://github.com/JulianZhan/market_mind/raw/refactoring/project_architecture/overall_architecture.jpg)

The diagram above provides architecture of Market Mind's web appplication and data pipelines. 

All servers are containerized into Docker containers, which are managed and deployed mainy through AWS ECS and Fargate as Docker hosting solution.

Market trades - Polygon.io API is used to stream BTC price data, which is then received by a Python producer and sent to message broker - Kafka. On the other side, Spark Structured Streaming is used to process the data and send to RDS MySQL for storage to achieve realtime streaming.

Market sentiment and emotion - Alpha Vantage API is used as market sentiment data source, and Reddit comments are crawled by PRAW and analyzed by LLM for market emotion. The market sentiment and emotion data is then sent to RDS MySQL for storage.
The sentiment and emotion batch pipelines are orchestrated by Airflow, which is deployed with docker-compose on an EC2 instance for easy deployment and management. Airflow is purely used for scheduling and orchestrating the batch pipelines daily, and the real computation is done by ECS Fargate containers. To achieve emotion analysis, LLM is deployed on SageMaker and called by ECS Fargate containers for serverless inference.

Database - RDS MySQL is choosed because of its schema-on-read feature, which provides strong data consistency, and cost-effectiveness. For scalability, RDS MySQL is also highly scalable with current leader and followers set up.

API Server - Flask is used as API server to provide data for users to access. Flask also listens to Kafka for realtime streaming data, which allows users to get realtime streaming trades through WebSocket connection. 

Web Backend - Spring Boot with Java is used as web backend to provide data for frontend page. Spring Boot framwork provides auto-configuration and dependency injection, which makes it easy to build and deploy. With integration of Spring Data JPA, connecting to RDS MySQL is managed though connection pool.

Web Frontend - React is used as web frontend to provide data visualization and user interaction. The combination of React and Spring Boot is popular and resourceful in terms of documentation. 



![Content Delivery Architecture](https://github.com/JulianZhan/market_mind/raw/refactoring/project_architecture/content_delivery_architecture.jpg)

![Servers Monitoring Architecture](https://github.com/JulianZhan/market_mind/raw/refactoring/project_architecture/servers_monitoring_architecture.jpg)

![Airflow Batch Pipelines Architecture](https://github.com/JulianZhan/market_mind/raw/refactoring/project_architecture/airflow_batch_pipelines_architecture.jpg)
