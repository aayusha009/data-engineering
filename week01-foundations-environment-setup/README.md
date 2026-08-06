# Week 1: Foundations + Environment Setup

## What I did this week
Learned the modern data stack flow: sources to ingestion to load to dbt run to query.
Reviewed key distinctions: data engineer vs analytics engineer vs analyst vs ML engineer, batch vs streaming, warehouse vs lake vs lakehouse, OLTP vs OLAP, row vs columnar storage.
Set up local environment: Homebrew, Git, Python 3.11, VS Code, Docker Desktop, PostgreSQL, pgAdmin.
Created GitHub repo (data engineering) to track all 10 weeks of work.
Drew architecture diagram: Sources to Raw storage to Warehouse to dbt models to Dashboards.

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
| PostgreSQL | 17 (EDB install) |
| VS Code | 1.131.0 |
| pgAdmin | 9.3 |

## Deliverables
GitHub repo with README: done
Environment installed and verified (see tech stack screenshots): done
Architecture diagram: done
This README: done
