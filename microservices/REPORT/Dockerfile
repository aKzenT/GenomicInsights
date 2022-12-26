FROM python:latest

RUN mkdir /results /script /report

COPY requirements.txt .


RUN apt-get clean && apt-get update && apt-get install build-essential python3-dev git wget software-properties-common ca-certificates -y
RUN git clone https://github.com/edenhill/librdkafka
RUN cd librdkafka && ./configure && make && make install && ldconfig
RUN cd ..

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY report.py /script/report.py

CMD [ "python3", "/script/report.py"]


