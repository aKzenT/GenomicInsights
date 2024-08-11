FROM apache/airflow:2.9.3-python3.11

# Copy requirements file
COPY requirements.txt .

# Switch to root user
USER 0

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

# Switch back to non-root user
USER 50000
RUN pip3 install --root-user-action ignore -r requirements.txt
