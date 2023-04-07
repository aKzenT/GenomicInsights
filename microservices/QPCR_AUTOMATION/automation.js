// Imports
import fs from 'fs';
import {Curl} from 'node-libcurl';
import querystring from 'querystring';
import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

// Read configuration data
const config = JSON.parse(fs.readFileSync('./config.json'));

function qpcr_automation(file) {
    dotenv.config();

    // Request to analysis endpoint 

    const curlRequest = new Curl();
    const terminate = curlRequest.close.bind(curlRequest);

    curlRequest.setOpt(Curl.option.URL, `${config.apiURL}/analysis?id=${config.analysisID}`);
    curlRequest.setOpt(Curl.option.HTTPPOST, [
        { name: 'f', file: `${config.watch_directory}/${file}`, type: 'text/xml' }
    ]);

    curlRequest.on("end", function (statusCode, data, headers) {
        //Store json response
        requestReport(data, config, file);
      this.close();
    });
    curlRequest.on("error", terminate);
    curlRequest.perform();
  }

export default {qpcr_automation};

// Request to report endpoint
function requestReport(analysisResults, config, file) {
    const curlReport = new Curl();
    const terminate = curlReport.close.bind(curlReport);

    curlReport.setOpt(Curl.option.URL, `${config.apiURL}/report?id=${config.analysisID}`);
    curlReport.setOpt(Curl.option.POST, true);
    curlReport.setOpt(Curl.option.POSTFIELDS, querystring.stringify({
        req: analysisResults,
      }));

    curlReport.on("end", function(statusCode, data, headers) {
        // Store response in html file
        const reportName = file.split('.')[0] + '_report.html';
        fs.writeFileSync(`${config.report_directory}/${reportName}`, data)
        sendEmail(`${config.report_directory}/${reportName}`);
        this.close();
    });
    curlReport.on("error", terminate);
    curlReport.perform();
}


// Send file as attachment via email

function sendEmail(path) {
  const mailFrom = process.env.EMAIL_FROM;
  const mailTo = process.env.EMAIL_TO;
  const pw = process.env.PASSWORD;
  const service = process.env.SERVICE;

  const transporter = nodemailer.createTransport({
    service: service,
    auth: {
    user: mailFrom,
    pass: pw
    }
  });
  const mailOptions = {
    from: mailFrom,
    to: mailTo,
    subject: 'qPCR analysis report',
    text: 'See the qPCR analysis report attached.',
    attachments: [{path}]
    
  };
  
  transporter.sendMail(mailOptions, function(error, info){
    if (error) {
      console.log(error);
    } else {
      console.log('Email sent: ' + info.response);
    }
  }); 
}





