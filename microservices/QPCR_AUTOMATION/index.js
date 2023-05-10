import Kafka from 'node-rdkafka';
import automation from  './automation.js';

const consumer = Kafka.KafkaConsumer({
  'group.id': 'kafka',
  'metadata.broker.list': 'localhost:29092'
}, {});

consumer.connect();

consumer.on('ready', () => {
  consumer.subscribe(['qpcr_automation_requested']);
  consumer.consume();
}).on('data', (data) => {
    const dataValue = JSON.parse(data.value.toString('utf-8'));
    if (dataValue.request === 'analyze') {
      console.log('analyze');
      automation.qpcr_automation(dataValue.file);
    }
    if (dataValue.request === 'report') {
      console.log('report');
      automation.requestReport();
    }
    if (dataValue.request === 'email') {
      console.log('email');
      automation.sendEmail();
    }
});






