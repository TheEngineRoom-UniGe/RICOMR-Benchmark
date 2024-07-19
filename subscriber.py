#!/usr/bin/env python
import rospy
from std_msgs.msg import Header
import time, threading

average = 0.0
counter = 0
counter_througput = 0.0


def callback(msg):
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
    if counter == 1000:
        rospy.loginfo("Received message with latency: %f ns", average/100.0)
        counter = 0
        average = 0
        
def msg_throuput():
    global counter_througput
    print("Message delivered ",counter_througput)
    counter_througput = 0
    threading.Timer(1, msg_throuput).start()

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('chatter', Header, callback)
    msg_throuput()
    rospy.spin()

if __name__ == '__main__':
    listener()