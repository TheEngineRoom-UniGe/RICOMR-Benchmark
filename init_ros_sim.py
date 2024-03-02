import os
import threading
import time
import argparse, sys
from distutils.util import strtobool

def run_gazebo():
    os.system("roslaunch gazebo_ros empty_world.launch")

def spawn_robot(robot_id):
    os.system("roslaunch ur_gazebo ur5_crowd_bringup.launch namespace:={0}".format(robot_id))

#/opt/ros/noetic/share/ur5_moveit_config/launch/
#/opt/ros/noetic/share/ur_gazebo/launch

def main():

    parser=argparse.ArgumentParser()
    parser.add_argument("--robots", type=int,help="number of robots", default=1)
    
    args=parser.parse_args()

    gazebo = threading.Thread(target=run_gazebo, args=())
    gazebo.start()
    time.sleep(5)
    
    for x in range(args.robots):
        robot_spawner = threading.Thread(target=spawn_robot, args=[x])
        robot_spawner.start()
        time.sleep(1)


if __name__ == "__main__":
    main()

