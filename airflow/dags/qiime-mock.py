from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

with DAG(
    dag_id='QIIME-Mock',
    default_args=default_args,
    schedule_interval=None,
    description='Mock for QIIME-Microservice',
    catchup=False,
    tags=['mock', 'fastapi', 'genomic'],
) as dag:

    t1 = SimpleHttpOperator(
        task_id='QIIME-Mock',
        http_conn_id='fastapi_service',
        endpoint='mock-workflow/test-workflow',
        method='POST',
        headers={"Content-Type": "application/json"},
        response_check=lambda response: response.status_code == 200,
        log_response=True
    )

    t2 = DummyOperator(
        task_id='done'
    )

    t1 >> t2
