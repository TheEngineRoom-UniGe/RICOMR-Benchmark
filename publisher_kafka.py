#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Header
import time
from interfaces.kafka_producer import KafkaProducer
from interfaces.kafka_admin import KafkaAdmin
import time, threading

counter_througput=0

def msg_throuput():
    global counter_througput
    print("Message delivered ",counter_througput)
    counter_througput = 0
    if rospy.is_shutdown():
        print("shutting down...")
    threading.Timer(1, msg_throuput).start()
    
def talker():
    global counter_througput
    kafka_bootstrap_server='SASL_PLAINTEXT://172.31.35.29:9096,SASL_PLAINTEXT://172.31.35.29:9097,SASL_PLAINTEXT://172.31.35.29:9098'
    kafka_key='theengineroom'
    kafka_secret='1tYdZP43t20'
    kafka_Topic = "benchmarking_topic"
    rospy.init_node('talker', anonymous=True)
    kafka_producer = KafkaProducer(bootstrap_serv=kafka_bootstrap_server,api_key= kafka_key,api_secret= kafka_secret)
    kafka_admin = KafkaAdmin(bootstrap_serv= kafka_bootstrap_server,api_key= kafka_key,api_secret= kafka_secret)
    kafka_admin.create_topic(kafka_Topic)

    rate = rospy.Rate(500)  # 10hz
    while not rospy.is_shutdown():
        msg_pub = Header()
        msg_pub.stamp = rospy.Time.now()
        msg_pub.frame_id = ""
        msg_pub.seq = 0
        counter_througput = counter_througput +1
        kafka_producer.produce_record(topic=kafka_Topic,msg=msg_pub)
        rate.sleep()

if __name__ == '__main__':
    try:
        msg_throuput()
        talker()
    except rospy.ROSInterruptException:
        pass
