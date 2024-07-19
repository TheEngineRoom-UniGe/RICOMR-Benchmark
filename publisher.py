#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Header
import time

def talker():
    pub = rospy.Publisher('chatter', Header, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1000)  # 10hz
    while not rospy.is_shutdown():
        current_time = rospy.Time.now()
        msg = Header()
        msg.stamp = rospy.Time.now()
        msg.frame_id = ""
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass