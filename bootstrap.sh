#!/bin/sh

#sudo apt-get install curl
#curl -s {s3}/bootstrap.sh | bash
cd ~
git clone https://github.com/TheEngineRoom-UniGe/RICOMR-Benchmark
cd RICOMR-Benchmark
sudo apt-get update
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt install curl -y
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo apt update -y
sudo apt install ros-noetic-desktop-full -y
source /opt/ros/noetic/setup.bash
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential -y
sudo apt install python3-rosdep
sudo rosdep init
rosdep update
sudo apt-get install ros-noetic-ur-gazebo -y
sudo apt-get install ros-noetic-ur5-moveit-config -y
sudo apt-get install ros-noetic-ur5-moveit-config -y
sudo apt-get install python3-pip -y
pip install -r requirements.yml
sudo cp ./moveit_crowd.launch /opt/ros/noetic/share/ur5_moveit_config/launch/
sudo cp ./moveit_planning_execution.launch /opt/ros/noetic/share/ur5_moveit_config/launch/
sudo cp ./ur5_crowd_bringup.launch /opt/ros/noetic/share/ur_gazebo/launch/