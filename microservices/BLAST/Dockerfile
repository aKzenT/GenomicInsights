FROM ncbi/blast:latest

RUN mkdir /blast/db /blast/raw /blast/results /script

COPY requirements.txt .

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get clean && apt-get update && apt-get install build-essential python3-dev git wget software-properties-common ca-certificates -y
RUN git clone https://github.com/edenhill/librdkafka
RUN cd librdkafka && ./configure && make && make install && ldconfig
RUN cd ..
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY blast.py /script/blast.py

CMD [ "python3", "/script/blast.py"]


