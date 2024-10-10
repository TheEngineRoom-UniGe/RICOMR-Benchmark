cd ~
git clone https://github.com/TheEngineRoom-UniGe/RICOMR-Benchmark
sudo apt install curl -y
cp -r ~/RICOMR-Benchmark/ROS2 ~/benchmark_ws


sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

sudo apt install software-properties-common
sudo add-apt-repository universe


sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update

sudo apt install ros-galactic-desktop python3-argcomplete
sudo apt install ros-dev-tools
sudo echo "source /opt/ros/galactic/setup.bash" > ~/.bashrc
sudo echo "export CYCLONEDDS_URI=/home/ubuntu/cyclone_profile.xml" > ~/.bashrc
sudo echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" > ~/.bashrc

sudo apt install ros-galactic-control*
sudo apt install ros-galactic-moveit*
sudo apt install ros-galactic-gazebo-ros*
sudo apt install ros-galactic-nav2*
sudo apt install ros-galactic-rmw-cyclonedds-cpp

cd ~/benchmark_ws
colcon build --symlink-install
source ./install/setup.bash
sudo echo "source /home/ubuntu/benchmark_ws/install/setup.bash" > ~/.bashrc
