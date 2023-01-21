
from time import sleep
from json import dumps, loads
import logging
from kafka import KafkaConsumer, KafkaProducer
from threading import Thread
import json
import os
import kafka
import sys
from fpdf import FPDF
import textwrap
import statistics
import io
import matplotlib.pyplot as plt
import PIL

result_folder = os.getenv('RESULT_FOLDER', default="/results/")
report_folder = os.getenv('RAW_FOLDER', default="/report/")
kafka_url = os.getenv('KAFKA_URL', default="kafka_kafka_1:9092")


a4_width_mm = 210
pt_to_mm = 0.35
margin_bottom_mm = 10
fontsize_pt = 10
character_width_mm = 7 * pt_to_mm
fontsize_mm = fontsize_pt * pt_to_mm
width_text = a4_width_mm / character_width_mm

stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [stdout_handler]

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('report')

kafka_brokers = [kafka_url]


kafka_consumer = KafkaConsumer(
    'report',
    bootstrap_servers=kafka_brokers,
    group_id='report',
    enable_auto_commit=True,
    partition_assignment_strategy=[
        kafka.coordinator.assignors.roundrobin.RoundRobinPartitionAssignor],
)

logger.info(kafka_consumer.bootstrap_connected)
logger.info(kafka_consumer.beginning_offsets)


kafka_producer = KafkaProducer(bootstrap_servers=kafka_brokers)


def create_report(data):
    logger.info("starting report " + data)
    data_json = json.loads(data)
    result_file = result_folder + "result_" + \
        data_json['file']+"_"+data_json['id']
    report_file = report_folder + "report_" + \
        data_json['file']+"_"+data_json['id']+".pdf"

    pdf = create_pdf()
    result_pdf = ''

    if (data_json['workflow'] == "blast"):
        result_pdf = report_blast(pdf, result_file)

    elif (data_json['workflow'] == "gc"):
        result_pdf = report_gc(pdf, result_file)

    result_pdf.output(report_file, 'F')

    sleep(10)
    kafka_producer.send('report', key=b'Report', value=json.dumps(
        {"id": data_json['id'], "Status": "successfull"}).encode('gbk'))
    logger.info("finished report " + data)


def create_pdf():

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    return pdf


def report_blast(pdf, result_file):

    pdf.set_font(family='Courier', size=20, style='B')
    file = open(result_file)
    text = file.read()
    splitted = text.split('\n')
    header = "TestREPORT"
    pdf.cell(0, fontsize_mm, header, ln=1, align='C')
    pdf.set_font(family='Courier', size=fontsize_pt)
    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    return pdf


def report_gc(pdf, result_file):
    gc_values = []
    with open(result_file, 'r') as fp:
        for line in fp:
            gc_value = line[:-1]
            gc_values.append(float(gc_value))

    gc_value_mean = statistics.mean(gc_values)

    xaxis = gc_values
    yaxis = range(0, len(gc_values))
    plt.xlabel('GC-Value in %')
    plt.ylabel('Sequencenumber')
    plt.plot(xaxis, yaxis)

    buf = io.BytesIO()
    plt.savefig(buf, dpi=300)
    buf.seek(0)
    PIL.Image.open(buf)

    pdf.set_font(family='Courier', size=20, style='B')
    header = "Report GC-Content"
    pdf.cell(0, fontsize_mm, header, ln=1, align='C')
    pdf.ln(4)
    pdf.set_font(family='Courier', size=fontsize_pt)

    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 6, '%s : %s' %
             ("GC-Content", str(round(gc_value_mean, 2)) + "%"), 0, 1, 'L', 1)
    pdf.ln(4)
    pdf.image(PIL.Image.open(buf), w=pdf.epw)
    return pdf


for message in kafka_consumer:
    if ('Status' in json.loads(message.value.decode("utf-8"))):
        continue
    Thread(target=create_report, args=(
        message.value.decode("utf-8"),), daemon=True).start()
    sleep(5)
