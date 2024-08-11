FROM quay.io/qiime2/amplicon:2023.9
#FROM python:3.11

RUN mkdir /db /raw /results /script

COPY requirements.txt .


# Install necessary dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    python3-dev \
    git \
    wget \
    software-properties-common \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install librdkafka
RUN git clone https://github.com/edenhill/librdkafka && \
    cd librdkafka && \
    ./configure && make && make install && ldconfig

# Upgrade pip and install Python packages
RUN pip3 install --upgrade pip
RUN pip3 install --root-user-action ignore -r requirements.txt

COPY qiime2_helpers.py /script/qiime2_helpers.py
COPY qiime2config.yml /script/qiime2config.yml
COPY qiime2_microbiome.py /script/qiime2_microbiome.py
COPY run_qiime2_analysis.sh /script/run_qiime2_analysis.sh

CMD [ "python3", "-u", "/script/qiime2_microbiome.py"]
