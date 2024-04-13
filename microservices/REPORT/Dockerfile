FROM python:3.11

RUN mkdir /results /script /report

COPY requirements.txt .


RUN apt-get clean && apt-get update && apt-get install build-essential python3-dev git wget software-properties-common ca-certificates -y
RUN git clone https://github.com/edenhill/librdkafka
RUN cd librdkafka && ./configure && make && make install && ldconfig
RUN cd ..

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY qiime2_expert_knowledge.txt /script/qiime2_expert_knowledge.txt
COPY report_helper.py /script/report_helper.py
COPY report.py /script/report.py

CMD [ "python3", "/script/report.py"]


