#!/usr/bin/env python
from std_msgs.msg import Header
import time, threading
from confluent_kafka import Consumer, KafkaError
from rospy_message_converter import message_converter
from interfaces.kafka_producer import KafkaProducer


def callback(msg):

    if msg.seq == 1:
        return
        
    global pub
    msg.seq = 1
    pub.publish(msg)


def listener():
    kafka_bootstrap_server='SASL_PLAINTEXT://172.31.35.29:9093,SASL_PLAINTEXT://172.31.35.29:9094,SASL_PLAINTEXT://172.31.35.29:9095'
    kafka_key='theengineroom'
    kafka_secret='1tYdZP43t20'
    kafka_Topic = "benchmarking_topic"

    consumer = Consumer({
    'bootstrap.servers': kafka_bootstrap_server,
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': kafka_key,
    'sasl.password': kafka_secret,
    'group.id': 'stock_price_group',
    'auto.offset.reset': 'latest',  # Start from the latest message
})
    kafka_producer = KafkaProducer(bootstrap_serv=kafka_bootstrap_server,api_key= kafka_key,api_secret= kafka_secret)
    consumer.subscribe([kafka_Topic])
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f'Error while consuming: {msg.error()}')
            else:
                message = message_converter.convert_dictionary_to_ros_message('std_msgs/Header', msg.value().decode('utf-8'))
                message.seq = 1
                kafka_producer.produce_record(message)


    except KeyboardInterrupt:
        pass
    finally:
    # Close the consumer gracefully
        consumer.close()

if __name__ == '__main__':
    listener()
