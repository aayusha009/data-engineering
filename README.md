# Learning outcomes

Week 1: Foundations + Environment Setup

Learned the modern data stack flow: sources -> ingestion -> load -> dbt run -> query, 
- Set up my local environment (Git, Python, Docker, PostgreSQL, VS Code, pgAdmin), created this GitHub repo, and drew out the architecture diagram for modern data sracj

Week 2: SQL for Data Engineering

- Practiced SQL against a real relational database (PostgreSQL, dvdrental) — writing queries, understanding schema structure and psql.

Week 3: Python Production Pipelines

- Built a working data pipeline in Python: pulled data from an API, saved the untouched raw response separately from the cleaned/validated version, added logging and pushed it to GitHub as a working repo.

Week 4: Data Modeling for Analytics

- Learned dimensional modeling — facts, dimensions, grain, star vs snowflake schema, measures, and Slowly Changing Dimensions (Types 1/2/3). Applied it by designing a  simple star schema for a College enrollment domain: wrote the SQL DDL, built a schema diagram. 

Week 5: Data Warehousing and Cost-Aware Querying

Created 30 days of sample order data with Python, saved it as Parquet, and loaded it into MotherDuck, a cloud data warehouse. Practiced writing SQL queries against it, and compared a full table scan to a query filtered by date, learning that filtering touches much less data and is far cheaper, which is why partitioning matters in a data warehouse.

Week 6: Data Transformation with dbt

Used dbt to clean and organize the orders data from Week 5's warehouse. Built a staging model that pulls the raw columns, an intermediate model that cleans up text formatting and removes bad rows, and final models that build a proper star schema with customer and product dimension tables plus an orders fact table, applying the data modeling ideas from Week 4. Also added 26 dbt tests checking things like uniqueness, required fields, and correct relationships between tables, all passing.

Week 7: Workflow Orchestration with Airflow

Used Apache Airflow, running locally through Docker, to schedule and orchestrate data pipelines. Set up Postgres as the metadata database and Redis with Celery to manage tasks across the webserver, scheduler, worker, and triggerer components.

Week 8: Docker, CI/CD, and Data Quality

Learned to containerize applications with Docker, set up basic CI/CD workflows, and apply data quality checks to catch bad data before it moves downstream.

Week 9: PySpark and Distributed Processing

Built a full PySpark pipeline using real taxi trip data, over 3.5 million rows. Read the data, cleaned invalid rows, joined it with a lookup table using a broadcast join, aggregated results by date and borough, and wrote the final output to Parquet. Used the Spark UI to see where a shuffle happened during aggregation.

Week 10: Kafka and Streaming

Learned core streaming concepts like topics, partitions, producers, consumers, and delivery semantics. Ran Kafka locally with Docker, created a topic, and built a producer and consumer in Python. Also compared message ordering between a single partition topic and a multi partition topic to see how partitioning affects order.

## Stacks used till now 

- Python
- PostgreSQL
- Git
- VS Code
- dbdiagram.io
- MotherDuck
- dbt
- Docker
- Apache Airflow
- PySpark
- Apache Kafka
