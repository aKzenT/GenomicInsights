import airflow
import json

from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from kafka import KafkaProducer
from datetime import datetime, timedelta

import shutil
import os

default_dag_args = {
    'start_date': datetime(2023, 4, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}    

def qpcr_automation_request():
    # Store file in new directory and rename it
    source_dir = 'qpcr_automation'
    target_dir = 'qpcr_automation_store'

    file_names = os.listdir(source_dir)
    for file_name in file_names:
        fn, file_extension = os.path.splitext(file_name);
        new_file_name = datetime.now().strftime("%Y_%m_%d__%H_%M_%S") + file_extension
        os.rename(os.path.join(source_dir, file_name), os.path.join(source_dir, new_file_name))
        if os.path.exists(os.path.join(target_dir, new_file_name)):
            os.remove(os.path.join(target_dir, new_file_name))
        shutil.move(os.path.join(source_dir, new_file_name), target_dir)
        # Produce event and send filename to consumer
        kafka_producer = KafkaProducer(bootstrap_servers=['kafka_kafka_1:9092'])
        kafka_producer.send('qpcr_automation_requested', value=json.dumps({"file":new_file_name}).encode('gbk'))

with airflow.DAG(
        'QPCR_Automation',
        schedule='@once',
        default_args=default_dag_args) as dag:

    t1 = FileSensor(
        task_id="wait_for_file", 
        filepath="qpcr_automation/", 
        fs_conn_id="my_file_system", 
        poke_interval= 30,
        dag=dag
    )

    t2 = PythonOperator(
        task_id='qpcr_automation_request',
        python_callable=qpcr_automation_request,
        dag=dag
    ) 

    t3 = TriggerDagRunOperator(
        task_id='reschedule_dag',
        trigger_dag_id='QPCR_Automation',
        reset_dag_run=True,
        dag=dag
    )
    
    t1 >> t2 >> t3
