# Start automation microservice

1. cd microservices/QPCR_AUTOMATION
2. npm install
3. Provide .env file with the following sturcture:

    SERVICE=service (# e.g. gmail)
    EMAIL_FROM=example_mail_from@gmail.com
    PASSWORD=password (* see instructions below)
    EMAIL_TO=example_mail_to@yahoo.com

    (* For gmail create password with the accepted answer of the following stackoverflow discussion: https://stackoverflow.com/questions/71477637/nodemailer-and-gmail-after-may-30-2022)

4. Fill the config.json to your needs. The default directories for watch_directory and store_directory are already provided in the airflow docker container. 
   If you want to use different directories make sure they exist.
5. npm start
6. Make sure that the qpcrAnalysisAPI is running, otherwise the automation process will fail.
7. Paste the xml files with the calculated Cq values you want to analyse in the watch_directory.
