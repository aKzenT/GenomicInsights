FROM ncbi/blast:latest

RUN mkdir /blast/db /blast/raw /blast/results /script

COPY requirements.txt .


# Install necessary dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
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

COPY blast.py /script/blast.py

CMD [ "python3", "/script/blast.py"]


