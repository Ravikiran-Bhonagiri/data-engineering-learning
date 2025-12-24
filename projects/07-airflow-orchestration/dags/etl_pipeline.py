from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import random

def _extract_data():
    """Simulates extracting data from an API."""
    print("Extracting data...")
    return random.choice(['data_available', 'no_data'])

def _check_availability(ti):
    """Decides which path to take based on extraction result."""
    status = ti.xcom_pull(task_ids='extract_task')
    if status == 'data_available':
        return 'transform_task'
    else:
        return 'skip_processing'

def _transform_data():
    print("Transforming data...")

default_args = {
    'owner': 'data_engineer',
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    'example_etl_pipeline',
    default_args=default_args,
    description='A conceptual DAG demonstrating branching and dependencies',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False
) as dag:

    start = BashOperator(
        task_id='start_pipeline',
        bash_command='echo "Starting Pipeline"'
    )

    # 1. Extraction Task (Push result to XComs)
    extract = PythonOperator(
        task_id='extract_task',
        python_callable=_extract_data
    )

    # 2. Branching Logic
    branch = BranchPythonOperator(
        task_id='check_data_availability',
        python_callable=_check_availability
    )

    # 3a. Transformation Path
    transform = PythonOperator(
        task_id='transform_task',
        python_callable=_transform_data
    )

    # 3b. Skip Path
    skip = BashOperator(
        task_id='skip_processing',
        bash_command='echo "No data found, skipping..."'
    )

    end = BashOperator(
        task_id='end_pipeline',
        bash_command='echo "Pipeline Finished"',
        trigger_rule='none_failed_min_one_success' # Run if either path succeeds
    )

    # Define Dependencies (The ">>" operator)
    start >> extract >> branch
    branch >> [transform, skip] >> end
