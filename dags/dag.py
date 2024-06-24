from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable, XCom
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from airflow.exceptions import AirflowException
import pandas as pd
import pyarrow.parquet as pq
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

def load_parquet_batch(parquet_files):
    postgres_hook = PostgresHook(postgres_conn_id='postgres_localhost')
    engine = postgres_hook.get_sqlalchemy_engine()
    
    for parquet_file in parquet_files:
        df = pq.read_table(os.path.join('/opt/airflow/data_sample', parquet_file)).to_pandas()
        df.columns = ['department_name','sensor_serial','create_at','product_name','product_expire']
        df.to_sql('airflow', engine, if_exists='append', index=False)
    
    #set flag when finish
    context['ti'].xcom_push(key='batch_loaded', value=True)

def load_parquet_to_postgres():
    parquet_files = [f for f in os.listdir('/opt/airflow/data_sample') if f.endswith('.parquet')]
    
    # Use ThreadPoolExecutor for parallel processing
    batch_size = 1500  # Number of files per batch
    max_workers = 16   # Number of threads to use

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(parquet_files), batch_size):
            batch = parquet_files[i:i+batch_size]
            executor.submit(load_parquet_batch, batch)

def stop_dag(**context):
    # Check if the batch_loaded flag is set
    batch_loaded = context['ti'].xcom_pull(key='batch_loaded', task_ids='load_all_parquet_files')
    if batch_loaded:
        raise AirflowException("Stopping DAG as the task has finished.")

with DAG(
    dag_id = 'postgres_operator_2',
    default_args = default_args,
    start_date = datetime(2023,1,1),
    schedule_interval= None,
    catchup=False
) as dag:
    start_task = DummyOperator(task_id='start_task')

    t2 = PythonOperator(
    task_id='load_parquet_to_postgres',
    python_callable=load_parquet_to_postgres,
)

    stop_task = PythonOperator(
        task_id='stop_dag',
        python_callable=stop_dag,
        provide_context=True,
        trigger_rule='all_done',
        dag=dag,
    )

start_task >> t2 >> stop_task