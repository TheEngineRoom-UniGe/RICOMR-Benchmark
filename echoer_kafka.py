#!/usr/bin/env python
from std_msgs.msg import Header
import rospy
import time, threading
from confluent_kafka import Consumer, KafkaError
from rospy_message_converter import message_converter
from interfaces.kafka_producer import KafkaProducer
import json

counter_througput=0
shut_down=0

def msg_throuput():
    global counter_througput
    global shut_down
    print("Message delivered ",counter_througput)
    counter_througput = 0
    if shut_down == 1:
        print("shutting down...")
    else:
        threading.Timer(1, msg_throuput).start()
    
    
def callback(msg):

    if msg.seq == 1:
        return
        
    global pub
    msg.seq = 1
    pub.publish(msg)


def listener():
    global counter_througput
    global shut_down
    msg_throuput()
    rospy.init_node('test', anonymous=True)
    kafka_bootstrap_server='SASL_PLAINTEXT://172.31.35.29:9096,SASL_PLAINTEXT://172.31.35.29:9097,SASL_PLAINTEXT://172.31.35.29:9098'
    kafka_key='theengineroom'
    kafka_secret='1tYdZP43t20'
    kafka_Topic = "benchmarking_topic"

    consumer = Consumer({
    'bootstrap.servers': kafka_bootstrap_server,
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.username': kafka_key,
    'sasl.password': kafka_secret,
    'group.id': 'echoer_group',
    'auto.offset.reset': 'latest',  # Start from the latest message
    'fetch.min.bytes':'1'
})
    kafka_producer = KafkaProducer(bootstrap_serv=kafka_bootstrap_server,api_key= kafka_key,api_secret= kafka_secret)
    consumer.subscribe([kafka_Topic])
    try:
        while True:
            msg = consumer.poll(1)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f'Error while consuming: {msg.error()}')
            else:
                message = message_converter.convert_dictionary_to_ros_message('std_msgs/Header', json.loads(msg.value().decode('utf-8')))
                if message.seq == 0:
                    message.seq = 1
                    kafka_producer.produce_record(topic=kafka_Topic,msg=message)
                    counter_througput = counter_througput + 1
                process_time = rospy.Time.now().to_nsec()
                                


    except KeyboardInterrupt:
        pass
    finally:
    # Close the consumer gracefully
        consumer.close()
 
    shut_down = 1
    print("consumer shutting down...")

if __name__ == '__main__':
    listener()
