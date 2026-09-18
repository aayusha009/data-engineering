from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def extract_from_API():
    print("Data extracted from API")

def land_raw_data(**kwargs):
    execution_date = kwargs['ds']
    print(f"Landing raw data for {execution_date} - writing to raw/{execution_date}.json ")

def load_from_warehouse(**kwargs):
    execution_date = kwargs['ds']
    print(f"Loading warehouse data for {execution_date} - using INSERT ... ON CONFLICT (upsert) keyed on date, so re-running updates the existing row instead of inserting a duplicate")

def dbt_transformation():
    print("data transformed using dbt")

with DAG(
    dag_id = "etl_pipeline",
    start_date = datetime(2026,1, 1),
    schedule = None,
    catchup = False  # Airflow ignores all the missed history. No historical backfills automatically  
) as dag:

    extract_task = PythonOperator(task_id = "extract", python_callable = extract_from_API, retries = 2, retry_delay = timedelta(minutes = 1))
    land_task = PythonOperator(task_id = "land", python_callable = land_raw_data)
    load_task = PythonOperator(task_id = "load", python_callable = load_from_warehouse)
    dbt_task= PythonOperator(task_id = "dbt", python_callable = dbt_transformation)

    extract_task >> land_task >> load_task >> dbt_task #run tasks simultaneously, in order from left to right




    
    