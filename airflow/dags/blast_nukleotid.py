from asyncio import run_coroutine_threadsafe
from encodings import utf_8
import functools
import json
import logging
from datetime import datetime, timedelta
from multiprocessing import context
from multiprocessing.sharedctypes import Value

from datetime import datetime
from airflow import DAG
from airflow.sensors.python import PythonSensor
from airflow.operators.python import PythonOperator
from kafka import KafkaConsumer, KafkaProducer


default_args = {
    "owner": "airflow",
    "depend_on_past": False,
    "start_date": datetime(2021, 7, 20),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}



#consumer_logger = logging.getLogger("airflow")

def analyzer_sensor(run_id):
    kafka_consumer = KafkaConsumer(    
        'blast_report',
        bootstrap_servers = ['kafka-kafka-1:9092'],
        group_id = run_id,  
        enable_auto_commit = True,
     )  
    for message in kafka_consumer:

        print(message.value)
        message_json = json.loads(message.value)
        if message_json['id'] == run_id and message_json['Status'] == "successfull":
            print("Analyse done")
            return True

def report_sensor(run_id):
    kafka_consumer = KafkaConsumer(    
        'report',
        bootstrap_servers = ['kafka-kafka-1:9092'],
        group_id = run_id,  
        enable_auto_commit = True,
     )  
    for message in kafka_consumer:

        print(message.value)
        message_json = json.loads(message.value)
        if message_json['id'] == run_id and message_json['Status'] == "successfull":
            print("Report done")
            return True
             
    
def produce_blast_request(run_id, file):
    kafka_producer = KafkaProducer(bootstrap_servers=['kafka-kafka-1:9092'])
    kafka_producer.send('blast_analyzer', value=json.dumps({"id":run_id,"file":file}).encode('gbk'))


def produce_report_request(run_id, file):
    kafka_producer = KafkaProducer(bootstrap_servers=['kafka-kafka-1:9092'])
    kafka_producer.send('report', value=json.dumps({"id":run_id,"file":file,"workflow":"blast"}).encode('gbk'))


with DAG(
    "BLAST_NUKLEOTID",
    default_args=default_args,
    description="Analyse Nukleotidsequences with BLAST",
    schedule_interval=None,
    catchup=False,
    tags=["BLAST"],
    
) as dag:
 
    t1 = PythonOperator(
        task_id="BLAST_Analyse_Requested",     
        python_callable=produce_blast_request,
        op_kwargs={"run_id":"{{ run_id }}","file":"{{ dag_run.conf['file'] }}"},
    )

    t2 = PythonSensor(
        task_id="BLAST_Analyse_Finished",     
        python_callable=analyzer_sensor,
        op_kwargs={"run_id":"{{ run_id }}"},
    )

    t3 = PythonOperator(
        task_id="Report_Requested",     
        python_callable=produce_report_request,
        op_kwargs={"run_id":"{{ run_id }}","file":"{{ dag_run.conf['file'] }}"},
    )
    
    t4 = PythonSensor(
        task_id="Report_Finished",     
        python_callable=report_sensor,
        op_kwargs={"run_id":"{{ run_id }}"},
    )
    t1 >> t2 >> t3 >> t4



