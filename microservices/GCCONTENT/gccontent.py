
from Bio import SeqIO
from Bio.SeqUtils import GC
from time import sleep
from json import dumps, loads
import logging
from kafka import KafkaConsumer, KafkaProducer
from threading import Thread
import json
import os
import kafka
import sys

result_folder = os.getenv('RESULT_FOLDER', default="/results/")
raw_folder = os.getenv('RAW_FOLDER', default="/raw/")
kafka_url = os.getenv('KAFKA_URL', default="kafka_kafka_1:9092")

stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [stdout_handler]

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('gc_analyzer')

kafka_brokers = [kafka_url]


kafka_consumer = KafkaConsumer(
    'gc_analyzer',
    bootstrap_servers=kafka_brokers,
    group_id='gc',
    enable_auto_commit=True,
    partition_assignment_strategy=[
        kafka.coordinator.assignors.roundrobin.RoundRobinPartitionAssignor],
)

logger.info(kafka_consumer.bootstrap_connected)
logger.info(kafka_consumer.beginning_offsets)


kafka_producer = KafkaProducer(bootstrap_servers=kafka_brokers)


def analyze_gc(data):
    # Do Analyzing
    raw_folder
    data_json = json.loads(data)
    file = raw_folder + data_json['file']
    result_file = result_folder + "result_" + \
        data_json['file']+"_"+data_json['id']
    record_fastq = SeqIO.parse(file, "fastq")
    gc_values_sorted = sorted(GC(rec.seq) for rec in record_fastq)

    with open(result_file, 'w') as fp:
        for item in gc_values_sorted:
            fp.write("%s\n" % item)
        print('Done')
    kafka_producer.send('gc_report', key=b'Report_GC', value=json.dumps(
        {"id": data_json['id'], "Status": "successfull"}).encode('gbk'))


for message in kafka_consumer:
    Thread(target=analyze_gc, args=(
        message.value.decode("utf-8"),), daemon=True).start()
    sleep(5)
