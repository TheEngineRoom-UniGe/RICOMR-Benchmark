#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Header
import time
from interfaces.kafka_producer import KafkaProducer
from interfaces.kafka_admin import KafkaAdmin

def talker():
    kafka_bootstrap_server='SASL_PLAINTEXT://172.31.35.29:9093,SASL_PLAINTEXT://172.31.35.29:9094,SASL_PLAINTEXT://172.31.35.29:9095'
    kafka_key='theengineroom'
    kafka_secret='1tYdZP43t20'
    kafka_Topic = "benchmarking_topic"
    rospy.init_node('talker', anonymous=True)
    kafka_producer = KafkaProducer(bootstrap_serv=kafka_bootstrap_server,api_key= kafka_key,api_secret= kafka_secret)
    kafka_admin = KafkaAdmin(bootstrap_serv= kafka_bootstrap_server,api_key= kafka_key,api_secret= kafka_secret)
    kafka_admin.create_topic(kafka_Topic)

    rate = rospy.Rate(500)  # 10hz
    while not rospy.is_shutdown():
        msg = Header()
        msg.stamp = rospy.Time.now()
        msg.frame_id = ""
        msg.seq = 0
        kafka_producer.produce_record(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

