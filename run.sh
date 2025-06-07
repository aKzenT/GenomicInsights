#docker network create distributed_system_network

DC="docker compose"
$DC -f airflow/docker-compose.yml up -d
$DC -f frontend/docker-compose.yml up -d
$DC -f kafka/docker-compose.yml up -d
$DC -f microservices/BLAST/docker-compose.yml up -d
$DC -f microservices/GCCONTENT/docker-compose.yml up -d
$DC -f microservices/QIIME2/docker-compose.yml up -d
$DC -f microservices/QPCR_AUTOMATION/docker-compose.yml up -d
$DC -f microservices/REPORT/docker-compose.yml up -d
$DC -f microservices/STORAGE/docker-compose.yml up -d
$DC -f docker-hadoop/docker-compose.yml up -d

curl --fail \
    --connect-timeout 5 \
    --max-time 10 \
    --retry 5 \
    --retry-delay 0 \
    --retry-max-time 40 \
    'http://localhost:880/'