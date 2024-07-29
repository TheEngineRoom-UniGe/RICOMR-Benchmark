import os
import threading
import time
import argparse, sys
from distutils.util import strtobool
import rospy
from std_msgs.msg import Header
import time, threading
import uuid

def echo_topic(topic_id):
    group=str(uuid.uuid1())
    os.system("kafkacat -b 'SASL_PLAINTEXT://172.31.35.29:9096,SASL_PLAINTEXT://172.31.35.29:9097,SASL_PLAINTEXT://172.31.35.29:9098' -L -X security.protocol=SASL_PLAINTEXT -X sasl.mechanisms=PLAIN -X sasl.username=theengineroom -X sasl.password=1tYdZP43t20 -G test_{0} benchmarking_topic".format(group))


def msg_throuput():
    counter = 0
    topic_listener = threading.Thread(target=echo_topic, args=[counter])
    topic_listener.start()
    threading.Timer(5, msg_throuput).start()
    counter = counter + 1

if __name__ == "__main__":
    msg_throuput()
