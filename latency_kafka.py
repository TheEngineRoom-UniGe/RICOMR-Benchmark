#!/usr/bin/env python
import rospy
from std_msgs.msg import Header
import time, threading
from confluent_kafka import Consumer, KafkaError
import json
from rospy_message_converter import message_converter

average = 0.0
counter = 0
counter_througput = 0.0
file_latency = open("latency.csv", "a")  # append mode

shut_down=0


def callback(msg):

    if msg.seq == 0:
        return
        
    global average
    global counter
    global counter_througput
    receive_time = rospy.Time.now().to_nsec()
    send_time = msg.stamp.to_nsec()
    # Calculate the latency
    latency = receive_time - send_time
    counter = counter +1
    average = average + latency
    counter_througput = counter_througput +1
    if (counter % 10 == 0):
        file_latency = open("latency.csv", "a")  # append mode
        file_latency.write("{0},\n".format(latency))
        file_latency.close()
    if counter >= 500:
        rospy.loginfo("Received message with latency: %f ns", average/500.0)
        counter = 0
        average = 0
        
def msg_throuput():
    global shut_down
    global counter_througput
    print("Message delivered ",counter_througput)
    file_msg = open("delivered.csv", "a")  # append mode
    file_msg.write("{0},\n".format(counter_througput))
    file_msg.close()
    counter_througput = 0
    if rospy.is_shutdown():
        shut_down = 1
        print("shutting down...")
    else:
        threading.Timer(1, msg_throuput).start()

def listener():
    global shut_down
    rospy.init_node('talker', anonymous=True)
    msg_throuput()
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
    'group.id': 'latency_group',
    'auto.offset.reset': 'latest',  # Start from the latest message
    'fetch.min.bytes':'1'
})
    
    consumer.subscribe([kafka_Topic])
    try:
        while True:
        
            if shut_down == 1:
                print("consumer shutting down...")
                break
                
                
            msg = consumer.poll(0.1)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f'Error while consuming: {msg.error()}')  
            else:
                message = message_converter.convert_dictionary_to_ros_message('std_msgs/Header',  json.loads(msg.value().decode('utf-8')))
                callback(message)
                



    except KeyboardInterrupt:
        pass
    finally:
    # Close the consumer gracefully
        consumer.close()

if __name__ == '__main__':
    listener()
