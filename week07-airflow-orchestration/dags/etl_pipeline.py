from airflow import DAG #defining a pipeline
from airflow.operators.python import PythonOperator #pyoperator wraps a plain function into an airflow task
from datetime import datetime, timedelta #datetime for start date and timedelta for retry_delay

def extract_from_API(): #task1: pretend to fetch data from an external API
    print("Data extracted from API") # reads data and doesn't store anything 

def land_raw_data(**kwargs): #save the raw extracted data into the raw storage 
    # **kwargs lets Airflow hand us info about this specific run 
    execution_date = kwargs['ds'] #'ds' runs date
    print(f"Landing raw data for {execution_date} - writing to raw/{execution_date}.json ")

def load_from_warehouse(**kwargs): #Task3: load the landed data into the warehouse 
    execution_date = kwargs['ds']
    print(f"Loading warehouse data for {execution_date} - using INSERT ... ON CONFLICT (upsert) keyed on date, so re-running updates the existing row instead of inserting a duplicate")
   # upsert by date -> re-running updates the same row, no duplicate rows

def dbt_transformation(): # Task4: run dbt to transform/clean the data inside the warehouse
    print("data transformed using dbt")

with DAG(
    dag_id = "etl_pipeline", #unique name for the DAG
    start_date = datetime(2026,1, 1), #earliest date the dag is allowed to run from
    schedule = None, # no automatic schedule - runs only when triggered manually
    catchup = False  # Airflow ignores all the missed history. No historical backfills automatically  
) as dag:

    # define each task by wrapping a function in a PythonOperator

    extract_task = PythonOperator(task_id = "extract", python_callable = extract_from_API, retries = 2, retry_delay = timedelta(minutes = 1))
    land_task = PythonOperator(task_id = "land", python_callable = land_raw_data)
    load_task = PythonOperator(task_id = "load", python_callable = load_from_warehouse)
    dbt_task= PythonOperator(task_id = "dbt", python_callable = dbt_transformation)

    # set the order tasks run in: extract first, then land, then load, then dbt
    extract_task >> land_task >> load_task >> dbt_task #run tasks simultaneously, in order from left to right




    
    