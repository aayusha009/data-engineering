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

## Git — commit and push changes
```
git status
git add <file-or-folder>
git commit -m "message"
git pull
git push
```
