# week07-airflow-orchestration written deliverables

## DAG - etl_pipeline (dags/etl_pipeline.py)
## ENVIRONMENT - Apache Airflow 2.9.3m run locally via docker-compose

- Command used:
 - ** docker exec -it week07-airflow-orchestration-airflow-scheduler-1 ** \
  ** airflow dags backfill etl_pipeline -s 2026-01-01 -e 2026-01-05 **
•	airflow dags backfill — the CLI subcommand for backfilling
•	etl_pipeline — the target DAG's id
•	-s 2026-01-01 / -e 2026-01-05 — the start/end of the date range to backfill

- Prerequisite: Airflow's backfill command needs the DAG to have a real schedule and not (Schedule = None), because it needs a defined interval to know what dates exist. The .etl_pipeline is designed for schedule=None (manual-trigger only), so schedule was temporarily changed to "@daily" to run the backfill, then reverted back to 'None' afterward, since manual-trigger is this pipeline's intended design.

- Running the same backfill command twice didn't create duplicate runs. Airflow already knew "Jan 1-5 for this DAG" had been done, so it skipped re-doing them and only ran the new date I added (Jan 6). This shows Airflow itself avoids duplicate runs, on top of the duplicate-record protection built into the individual tasks.

## Idempotency checklist

Idempotency is only handled explicitly at the two points in the pipeline that actually write data (land, load); the read-only step (extract) and the tool with built-in idempotent behavior (dbt) don't need extra code. Combined with Airflow's own run-uniqueness guarantee, the DAG is safely re-runnable, manually, via retry, or via backfill without producing duplicate records.

# Airflow + Docker Commands Reference

Every command used to build, run, and test the `etl_pipeline` DAG, in the order
you'd typically use them.

## Start/restart the Airflow stack (Docker Compose)
```
docker-compose up -d
```

## Check container status
```
docker ps
```

## Verify the DAG file is visible inside the scheduler container
```
docker exec -it week07-airflow-orchestration-airflow-scheduler-1 ls /opt/airflow/dags
```

## Sanity-check the Airflow CLI is working
```
docker exec -it week07-airflow-orchestration-airflow-scheduler-1 airflow version
```

## Trigger a manual run (same as clicking "Trigger DAG" in the UI)
```
docker exec -it week07-airflow-orchestration-airflow-scheduler-1 airflow dags trigger etl_pipeline
```

## Run a backfill for a date range
```
docker exec -it week07-airflow-orchestration-airflow-scheduler-1 \
  airflow dags backfill etl_pipeline -s 2026-01-01 -e 2026-01-05
```

Common flags:
- `--reset-dagruns` — delete and recreate existing runs in that range before backfilling
- `-I` / `--ignore-first-depends-on-past` — skip depends_on_past check for the first day
- `--rerun-failed-tasks` — only re-run tasks that failed last time

## Check for DAG import/syntax errors without triggering anything
```
docker exec -it week07-airflow-orchestration-airflow-scheduler-1 airflow dags list-import-errors
```

## Stream live scheduler logs (useful for debugging a broken DAG)
```
docker logs -f week07-airflow-orchestration-airflow-scheduler-1
```
