# Week 1: Foundations + Environment Setup

## What I did this week
1. Learned the modern data stack flow: sources to ingestion to load to dbt run to query.
2. Understood that data engineers build and maintain pipelines, analytics engineer take raw data in warehouse and model it to clean and tested tables, data analysts query clean tables to answer business questions and create dashboards, reports, ML engineers make models on top of clean data. 
3. Set up local environment: Homebrew, Git, Python 3.11, VS Code, Docker Desktop, PostgreSQL, pgAdmin.
4. Created GitHub repo (data engineering) to track all 10 weeks of work.
5. Drew architecture diagram: Sources to Raw storage to Warehouse to dbt models to Dashboards.

## Architecture Overview

Sources: Sources are where the raw data gets generated, for example, from databases like MySQL or PostgreSQL (OLTP, Online Transaction Processing systems), CSV files, event logs, ad platforms, etc.

Ingestion: Data is pulled from the source and lands as raw storage, typically in storage like S3. Nothing is transformed at this stage, the data is stored exactly as it is. This step can run on a schedule, such as batch (separated into batches) or stream processing (continuous), depending on the needs.

Load: The raw data is now loaded into a data warehouse (Snowflake, Postgres). Data now becomes queryable using SQL, but it is still mostly in its original, raw shape and not ready for analysis.

dbt run: SQL transformations are executed and modeled against the warehouse tables. This stage is where the data gets cleaned, duplicates are removed, and data is reshaped into well structured tables that are finally ready for analysis.

Query: A BI tool such as Tableau or Power BI queries the clean dbt models and turns them into reports and dashboards that a business person can actually read and analyze.

## Environment
| Tool | Version |
|---|---|
| Git | 2.55.0 |
| Python | 3.11 |
| Docker | 29.6.2 |
| PostgreSQL | 17 |
| VS Code | 1.131.0 |
| pgAdmin | 9.3 |

## Deliverables
1. GitHub repo with README: done
2. Environment installed and verified (see tech stack screenshots): done
3. Architecture diagram: done
