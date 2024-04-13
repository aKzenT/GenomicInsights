from time import sleep
from json import dumps, loads
import logging
from kafka import KafkaConsumer, KafkaProducer
from threading import Thread
import json
import os
import kafka
import sys
import time
import subprocess
from pathlib import Path

#import self-written helper functions
from qiime2_helpers import createBarplotFromQIIME2qzv

result_folder = os.getenv('RESULT_FOLDER', default="/results/")
raw_folder = os.getenv('RAW_FOLDER', default="/raw/")
kafka_url = os.getenv('KAFKA_URL', default="kafka-kafka-1:9092")

stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [stdout_handler]

logging.basicConfig(
    level=logging.ERROR, #can also be set to DEBUG
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('qiime2_analyzer')

kafka_brokers = [kafka_url]

kafka_consumer = KafkaConsumer(
    'qiime2_analyzer',
    bootstrap_servers=kafka_brokers,
    group_id='qiime2',
    enable_auto_commit=True,
    partition_assignment_strategy=[kafka.coordinator.assignors.roundrobin.RoundRobinPartitionAssignor]
)

logger.info(kafka_consumer.bootstrap_connected)
logger.info(kafka_consumer.beginning_offsets)


kafka_producer = KafkaProducer(bootstrap_servers=kafka_brokers)

def analyze_qiime2(data):
    raw_folder
    data_json = json.loads(data)
    
    file = raw_folder + data_json['file']
    result_file = result_folder + "result_" + \
        data_json['file']+"_"+data_json['id']
    
    #perform analysis in QIIME2
    subp_res = subprocess.run(["/script/run_qiime2_analysis.sh", str(file), str(result_file)])

    print(subp_res)
    print(subp_res.returncode)

    if subp_res.returncode != 0:
        #exit with error 
        time.sleep(15) #sleep is needed for the error case --> otherwise it's too fast for kafka to handle events

        kafka_producer.send('qiime2_analysis_started', key=b'Report_QIIME2', value=json.dumps({"id":data_json['id'], "Status":"error"}).encode('gbk'))         
    else:
        #create barplot with python functionality defined in qiime_helpers.py
        #create directory                 
        Path(str(result_file) + "/" + "/python_barplots/").mkdir(parents=True, exist_ok=True)

        createBarplotFromQIIME2qzv(
            import_path = str(result_file) + "/" + "taxa-bar-plots.qzv", 
            export_path = str(result_file) + "/" + "/python_barplots/") 
    
        kafka_producer.send('qiime2_analysis_started', key=b'Report_QIIME2', value=json.dumps({"id":data_json['id'], "Status":"successfull"}).encode('gbk')) 
    

def qiime2_classification(data):
    data_json = json.loads(data)

    time.sleep(15) #sleep is needed for this now function (needs to be filled with functionality) --> otherwise it's too fast for kafka to handle events # TODO

    kafka_producer.send('qiime2_classification', key=b'Classification_QIIME2', value=json.dumps({"id":data_json['id'], "Status":"successfull"}).encode('gbk')) 


for message in kafka_consumer:
    message_json = json.loads(message.value)
    if 'Call' in message_json and message_json['Call'] == "StartAnalysis":
        Thread(target=analyze_qiime2, args=(message.value.decode("utf-8"),), daemon=True).start()
        sleep(5)
    elif 'Call' in message_json and message_json['Call'] == "StartClassification":
        Thread(target=qiime2_classification, args=(message.value.decode("utf-8"),), daemon=True).start()
        sleep(5)
