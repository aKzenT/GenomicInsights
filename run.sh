#docker network create distributed_system_network
docker compose -f airflow/docker-compose.yml up -d
docker compose -f frontend/docker-compose.yml up -d
docker compose -f kafka/docker-compose.yml up -d
docker compose -f microservices/BLAST/docker-compose.yml up -d
docker compose -f microservices/GCCONTENT/docker-compose.yml up -d
docker compose -f microservices/QIIME2/docker-compose.yml up -d
docker compose -f microservices/REPORT/docker-compose.yml up -d
docker compose -f microservices/STORAGE/docker-compose.yml up -d
