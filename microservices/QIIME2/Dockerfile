FROM quay.io/qiime2/amplicon:2023.9
#FROM python:3.11

RUN mkdir /db /raw /results /script

COPY requirements.txt .

RUN apt-get clean && apt-get update && apt-get install build-essential python3-dev git wget software-properties-common ca-certificates -y
RUN git clone https://github.com/edenhill/librdkafka
RUN cd librdkafka && ./configure && make && make install && ldconfig
RUN cd ..
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
#RUN git clone https://github.com/sbslee/dokdo
#RUN pip install dokdo/
#RUN rm -rf dokdo/

#RUN conda activate qiime2-amplicon-2023.9 #activate QIIME2 conda environment 

COPY qiime2_helpers.py /script/qiime2_helpers.py
COPY qiime2config.yml /script/qiime2config.yml
COPY qiime2_microbiome.py /script/qiime2_microbiome.py
COPY run_qiime2_analysis.sh /script/run_qiime2_analysis.sh

CMD [ "python3", "-u", "/script/qiime2_microbiome.py"]
