import os
import threading
import time
import argparse, sys
from distutils.util import strtobool
import rospy
from std_msgs.msg import Header
import time, threading

topics = ['/chatter']

def echo_topic(topic_id):
    os.system("rostopic echo {0}".format(topic_id))


def msg_throuput():
    topic_listener = threading.Thread(target=echo_topic, args=[topics[0]])
    topic_listener.start()
    threading.Timer(5, msg_throuput).start()


if __name__ == "__main__":
    msg_throuput()
