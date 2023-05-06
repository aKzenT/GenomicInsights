# Instructions
You will need docker installed on your machine to run this project. If you don't have it installed, you can download it [here](https://www.docker.com/products/docker-desktop).

Once you have docker installed, you can run the following commands to get the project up and running. First, you need a virtual network with the name "distributed_system_network" to run the project. You can create it with the following command:
```bash
docker network create distributed_system_network
```

## Starting and stopping the project
Then, you can run the following command to start all containers:
```bash
./run.sh
```

To stop all containers, you can run the following command:
```bash
./stop.sh
```

## Accessing the web application
After running the project, you can access the web application at http://localhost:880. You should also be able to access Apache Airflow at http://localhost:8080. The default user name and password is "airflow". In Airflow you can see the defined DAGs. Make sure to enable the DAGs you want to use by clicking on the toggle button on the left side of the DAG name.

## Configuring the BLAST databases
The BLAST workflow depends on the presence of BLAST database files in the data directory. As they are too big to be included in the repository, you will need to download them yourself. You can download the files from the [NCBI FTP server](https://ftp.ncbi.nlm.nih.gov/blast/db/). You'll need the https://ftp.ncbi.nlm.nih.gov/blast/db/nt.00.tar.gz file. The files need to be extracted and added to the data/BLAST_DATABASES/db directory.

## Running BLAST analysis
After opening the web application, choose the BLAST workflow and select one of the example files, "seq1" or "seq2". After submitting the workflow, you can watch the progress in Apache Airflow. After the workflow is finished, you can download the results from the web application.

## Running GC Content analysis
For the GC Content workflow, you should download a large FASTQ file for analysis. You can use the SRS012969 example file from the Human Microbiome Project which you can find here: https://portal.hmpdacc.org/files/596fc2de57601ec08a01fdee59b509b1 . After downloading the file and extracting the contents, you can upload the SRS012969.denovo_duplicates_marked.trimmed.1.fastq file to the web application. Alternatively, you can copy the data directly to the data/RAW directory. After submitting, you can watch the progress in Apache Airflow again. Keep in mind that the GC Content workflow takes a long time to run (about 40mins on my machine). After the workflow is finished, you can download the results from the web application.

## Running qPCR analysis workflow
TODO