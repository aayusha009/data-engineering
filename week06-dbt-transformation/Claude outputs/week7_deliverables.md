# Week 7 — Airflow Orchestration: Written Deliverables

**DAG:** `etl_pipeline` (`dags/etl_pipeline.py`)
**Environment:** Apache Airflow 2.9.3, run locally via Docker Compose (CeleryExecutor)

---

## Backfill Explanation

Backfill lets you retroactively create DAG runs for a range of past dates, as if the
DAG had been running on its schedule the whole time. It's used to reprocess historical
data — for example, after fixing a bug in a transformation, or bringing a new pipeline
"up to date" with data that predates when it was first turned on.

**Command used:**
```
docker exec -it week07-airflow-orchestration-airflow-scheduler-1 \
  airflow dags backfill etl_pipeline -s 2026-01-01 -e 2026-01-05
```

- `airflow dags backfill` — the CLI subcommand for backfilling
- `etl_pipeline` — the target DAG's id
- `-s 2026-01-01` / `-e 2026-01-05` — the start/end of the date range to backfill

**Prerequisite:** Airflow's backfill command requires the DAG to have a real `schedule`
(not `schedule=None`), since it needs a defined interval to know what logical dates
exist. `etl_pipeline` is designed for `schedule=None` (manual-trigger only), so
`schedule` was temporarily changed to `"@daily"` to run the backfill, then reverted
back to `None` afterward, since manual-trigger is this pipeline's intended design.

**Result:** the command created 5 separate DAG runs (`backfill__2026-01-01` through
`backfill__2026-01-05`), each executing the full `extract → land → load → dbt` chain.
All 20 task instances (5 runs × 4 tasks) completed with `state=success`, confirmed in
both the scheduler logs and the Airflow UI's Grid view (filtered by run type
"backfill").

**Idempotency observation from backfill itself:** re-running the same backfill command
a second time (and a third time with an extended range, `-e 2026-01-06`) did not
duplicate the already-completed runs — Airflow recognized `dag_id + run_id`
(which encodes the logical date) as already existing and successful, and only
processed the genuinely new date. This is Airflow's own built-in protection against
duplicate DAG runs, separate from the task-level idempotency described below.

---

## Idempotency Checklist

Idempotency means running the pipeline more than once for the same date produces the
same end state, not duplicated data. This matters because retries and backfill both
depend on tasks being safe to re-run.

| Task | Idempotency strategy | Why |
|---|---|---|
| `extract` (API call) | No idempotency handling needed | Read-only — fetches data but doesn't write/store anything itself, so there's nothing to duplicate. Safe to retry (`retries=2`) since a failed read has no side effect to undo. |
| `land` (raw storage) | Overwrite-by-date | Writes to a path keyed on the execution date (`raw/{ds}.json`). Re-running for the same date overwrites the same file instead of creating a new one. |
| `load` (warehouse) | Upsert-by-date | Uses `INSERT ... ON CONFLICT` (upsert) keyed on date. Re-running for the same date updates the existing row instead of inserting a duplicate. |
| `dbt` (transformation) | Idempotent by design | dbt rebuilds models from source (`CREATE OR REPLACE ... AS SELECT ...`), so `dbt run` produces the same table each time regardless of how many times it's executed — no extra code needed. |
| DAG run level | Airflow's `dag_id + run_id` uniqueness | Confirmed via backfill test above: re-running backfill over an overlapping date range didn't create duplicate DagRuns for dates already completed. |

**Summary:** idempotency is only handled explicitly at the two points in the pipeline
that actually write data (`land`, `load`); the read-only step (`extract`) and the
tool with built-in idempotent behavior (`dbt`) don't need extra code. Combined with
Airflow's own run-uniqueness guarantee, the DAG is safely re-runnable — manually,
via retry, or via backfill — without producing duplicate records.
