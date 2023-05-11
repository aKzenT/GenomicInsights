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

## Uploading Data
To make data available within the system, there is a separate menu item ("Upload Data") within the user interface of GenomicInsights. With this, a user can upload a file using "drag and drop" on the one hand or using the file browser on the other. In the background, the storage microservice /upload endpoint is used.

## Running Workflows
A user can start analyses via the "Start Analysis" menu item. In the upper area of the user interface, the different steps that have to be performed in order to start an analysis are shown. In the first step, a workflow must be selected. When loading, the Airflow API is addressed and all stored workflows are displayed with the corresponding description. If many workflows are stored in the system, finding a specific workflow can take a long time. For this reason, a search function is built in, which allows to filter the entries. The filter is based on the name of the workflow.

After the successful selection of the workflow, the available files are displayed in the next step. The listed files were returned by the storage microservice. If many files are stored in the system, finding a specific file can take a long time. For this reason, a search function is built in, which allows to filter the entries. Filtering is done by the name of the file.

In the last step, the user is shown the selections again and can then press the "Submit" button. In the background, the selected workflow is started via the Airflow API and the corresponding configuration is transferred. A pop-up appears asking the user to switch to the detailed view to follow his workflow.

The detailed view shows the current status of the workflow (which steps have already been completed and which step is currently being processed). This is done via polling of the Airflow API. The user can activate or deactivate the polling via a switch at the bottom right.

## Running BLAST analysis
To run a BLAST analysis, choose the BLAST workflow and select one of the example files, "seq1" or "seq2". After submitting the workflow, you can watch the progress in Apache Airflow. After the workflow is finished, you can download the results from the web application.

## Running GC Content analysis
For the GC Content workflow, you should download a large FASTQ file for analysis. You can use the SRS012969 example file from the Human Microbiome Project which you can find here: https://portal.hmpdacc.org/files/596fc2de57601ec08a01fdee59b509b1 . After downloading the file and extracting the contents, you can upload the SRS012969.denovo_duplicates_marked.trimmed.1.fastq file to the web application. Alternatively, you can copy the data directly to the data/RAW directory. After submitting, you can watch the progress in Apache Airflow again. Keep in mind that the GC Content workflow takes a long time to run (about 40mins on my machine). After the workflow is finished, you can download the results from the web application.

## Running qPCR analysis workflow
TODO