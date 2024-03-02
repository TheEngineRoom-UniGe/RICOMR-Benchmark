import os
import threading
import time
import argparse, sys
from distutils.util import strtobool



def moveit_config_ros(robot_id):
    os.system("roslaunch ur5_moveit_config moveit_planning_execution.launch sim:=true namespace:={0}".format(robot_id))

def moveit_config_kafka(robot_id):
    os.system("roslaunch ur5_moveit_config moveit_crowd.launch namespace:={0}".format(robot_id))

def spin_controllers(robot_id, is_ros):
    os.system("python3 ./interfaces/planning_execution.py --namespace={0} --ros={1}".format(robot_id,is_ros))

def main():

    parser=argparse.ArgumentParser()
    parser.add_argument("--robots", type=int,help="number of robots", default=1)
    parser.add_argument("--ros", help="set it to true to enable ROS interface",type=lambda x: bool(strtobool(x)) ,default=True)
    parser.add_argument("--start", type=int,help="id of starting robot", default=0)
    args=parser.parse_args()

    for x in range(args.start,args.robots):
        if args.ros:
            moveit_spawner = threading.Thread(target=moveit_config_ros, args=[x])
            moveit_spawner.start()
        else:
            moveit_spawner = threading.Thread(target=moveit_config_kafka, args=[x])
            moveit_spawner.start()
        
        time.sleep(2)

        robot_control_spawner = threading.Thread(target=spin_controllers, args=[x,args.ros])
        robot_control_spawner.start()
        

if __name__ == "__main__":
    main()