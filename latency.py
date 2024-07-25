#!/usr/bin/env python
import rospy
from std_msgs.msg import Header
import time, threading

average = 0.0
counter = 0
counter_througput = 0.0
file_latency = open("latency.csv", "a")  # append mode



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
        rospy.loginfo("Received message with latency: %f ns", average/100.0)
        counter = 0
        average = 0
        
def msg_throuput():
    global counter_througput
    print("Message delivered ",counter_througput)
    file_msg = open("delivered.csv", "a")  # append mode
    file_msg.write("{0},\n".format(counter_througput))
    file_msg.close()
    counter_througput = 0
    threading.Timer(1, msg_throuput).start()

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('chatter', Header, callback)
    msg_throuput()
    rospy.spin()

if __name__ == '__main__':
    listener()
