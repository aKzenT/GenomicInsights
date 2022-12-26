FROM apache/airflow:2.4.0
COPY requirements.txt .
USER 0
RUN sudo apt-get update
RUN sudo apt-get install build-essential python3-dev git wget software-properties-common ca-certificates -y
#RUN wget http://packages.confluent.io/deb/7.2/archive.key | sudo apt-key add archive.key
#RUN sudo add-apt-repository "deb [arch=amd64] http://packages.confluent.io/deb/7.2 stable main"
#RUN sudo add-apt-repository "deb http://packages.confluent.io/clients/deb $(lsb_release -cs) main"
#RUN sudo apt-get update && sudo apt-get install confluent-platform
#RUN apt update && apt -y install software-properties-common gcc
RUN git clone https://github.com/edenhill/librdkafka
RUN cd librdkafka && ./configure && make && make install && ldconfig
RUN pip3 install --upgrade pip
RUN pip3 install --root-user-action ignore -r requirements.txt
USER 50000
RUN pip3 install --root-user-action ignore -r requirements.txt
