#!/usr/bin/env python
import rospy
from std_msgs.msg import Header
import time, threading

pub = rospy.Publisher('chatter', Header, queue_size=100)

def callback(msg):

    if msg.seq == 1:
        return
        
    global pub
    msg.seq = 1
    pub.publish(msg)


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('chatter', Header, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
