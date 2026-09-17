from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def extract_from_API():
    print("Data extracted from API")

def land_raw_data():
    print("Landing raw data into raw storage")

def load_from_warehouse():
    print("Data loaded into the warehouse")

def dbt_transformation():
    print("data transformed using dbt")

with DAG(
    dag_id = "etl_pipeline", #unique name for the DAG 
    start_date = datetime(2026,1, 1),
    schedule = None #won't run automatically, only when i trigger it manually, it will run
) as dag:

    extract_task = PythonOperator(task_id = "extract", python_callable = extract_from_API)
    land_task = PythonOperator(task_id = "land", python_callable = land_raw_data)
    load_task = PythonOperator(task_id = "load", python_callable = load_from_warehouse)
    dbt_task= PythonOperator(task_id = "dbt", python_callable = dbt_transformation)

    extract_task >> land_task >> load_task >> dbt_task #run tasks simultaneously, in order from left to right




    
    