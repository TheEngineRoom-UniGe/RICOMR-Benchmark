from ros_interface import UR5Interface
from moveit_interface import  moveitInterface
import rospy
import argparse, sys
from distutils.util import strtobool


def main():

    parser=argparse.ArgumentParser()
    parser.add_argument("--namespace", help="robot namespace", default="0")
    parser.add_argument("--ros", help="set it to true to enable ROS interface",type=lambda x: bool(strtobool(x)) ,default=True)
    
    args=parser.parse_args()

    ur5_arm = moveitInterface(ns=args.namespace)

    ur5_interface = UR5Interface(ur5_arm, is_ros=args.ros, ns=args.namespace)
    

    while not rospy.is_shutdown():
       ur5_interface.main_routine()
         

if __name__ == '__main__':
  main()