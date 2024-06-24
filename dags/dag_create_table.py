from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id = 'postgres_operator_1',
    default_args = default_args,
    # start_date = datetime(2023,1,1),
    schedule_interval= None,
) as dag:
    t1 = PostgresOperator(
    task_id='create_table',
    postgres_conn_id = 'postgres_localhost',
    sql = """
        create table if not exists airflow(
            department_name varchar,
            sensor_serial varchar,
            create_at timestamp,
            product_name varchar,
            product_expire timestamp,
            rec integer
        )
    """
)
