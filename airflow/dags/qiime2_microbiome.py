#from asyncio import run_coroutine_threadsafe
#from encodings import utf_8
#import functools
import json
import logging
from datetime import datetime, timedelta
#from multiprocessing import context
#from multiprocessing.sharedctypes import Value

from airflow import DAG
from airflow.sensors.python import PythonSensor
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
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

logger = logging.getLogger(__name__)
logger.info("QIIME2 Microbiome Analysis DAG started")
#consumer_logger = logging.getLogger("airflow")

def python_sensor(run_id, topic):
    kafka_consumer = KafkaConsumer(
        topic, 
        bootstrap_servers = ['kafka-kafka-1:9092'],
        group_id = run_id,
        enable_auto_commit = True
     )  
    for message in kafka_consumer:
        logger.info("Received message from %s for run_id %s: %s", topic, run_id, message.value)

        message_json = json.loads(message.value)
        if message_json['id'] == run_id and 'Status' in message_json:
            if message_json['Status'] == "successfull":
                print("Analysis done")
                return True
            elif message_json['Status'] == "error":                
                raise AirflowFailException("Analysis failed with Error")


def report_sensor(run_id):
    kafka_consumer = KafkaConsumer(    
        'report',
        bootstrap_servers = ['kafka-kafka-1:9092'],
        group_id = run_id,         
        enable_auto_commit = True
     )  
    for message in kafka_consumer:
        logger.info("Received message from %s for run_id %s: %s", 'report', run_id, message.value)

        message_json = json.loads(message.value)
        if message_json['id'] == run_id and 'Status' in message_json:
            if message_json['Status'] == "successfull":
                print("Report done")
                return True             
            elif message_json['Status'] == "error":                
                raise AirflowFailException("Report creation failed with Error")
    
def produce_qiime2microbiome_request(run_id, file):
    logger.info("Producing message: %s, %s, %s", run_id, file, "StartAnalysis")

    kafka_producer = KafkaProducer(bootstrap_servers=['kafka-kafka-1:9092'])
    kafka_producer.send('qiime2_analyzer', value=json.dumps({"id":run_id,"file":file,"Call":"StartAnalysis"}).encode('gbk'))

def produce_sampleclassification_request(run_id, file):
    logger.info("Producing message: %s, %s, %s", run_id, file, "StartClassification")

    kafka_producer = KafkaProducer(bootstrap_servers=['kafka-kafka-1:9092'])
    kafka_producer.send('qiime2_analyzer', value=json.dumps({"id":run_id,"file":file,"Call":"StartClassification"}).encode('gbk')) 

def produce_report_request(run_id, file):
    logger.info("Producing report request: %s, %s, %s", run_id, file, "qiime2")
    kafka_producer = KafkaProducer(bootstrap_servers=['kafka-kafka-1:9092'])
    kafka_producer.send('report', value=json.dumps({"id":run_id,"file":file,"workflow":"qiime2"}).encode('gbk'))


with DAG(
    "QIIME2_MICROBIOME",
    default_args=default_args,
    description="Microbiome Composition Determination",
    schedule_interval=None,
    catchup=False,
    tags=["QIIME2"],
    
) as dag:
 
    t1 = PythonOperator(
        task_id="Microbiome_Analysis_Started",     
        python_callable=produce_qiime2microbiome_request,
        op_kwargs={"run_id":"{{ run_id }}","file":"{{ dag_run.conf['file'] }}"},
    )

    t2 = PythonSensor(
        task_id="Calculating_Relative_Abundances",     
        python_callable=python_sensor,
        op_kwargs={"run_id":"{{ run_id }}","topic":"qiime2_analysis_started"},
    )

    t3 = PythonOperator(
        task_id="Sample_Classification_Started",     
        python_callable=produce_sampleclassification_request,
        op_kwargs={"run_id":"{{ run_id }}","file":"{{ dag_run.conf['file'] }}"},
    )

    t4 = PythonSensor(
        task_id="Sample_Classification_Done",     
        python_callable=python_sensor,
        op_kwargs={"run_id":"{{ run_id }}","topic":"qiime2_classification"},
    )

    t5 = PythonOperator(
        task_id="Report_Generation_Started",     
        python_callable=produce_report_request,
        op_kwargs={"run_id":"{{ run_id }}","file":"{{ dag_run.conf['file'] }}"},
    )
    
    t6 = PythonSensor(
        task_id="Report_Generation_Done",     
        python_callable=report_sensor,
        op_kwargs={"run_id":"{{ run_id }}"},
    )
    t1 >> t2 >> t3 >> t4 >> t5 >> t6



