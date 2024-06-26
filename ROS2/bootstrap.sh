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

sudo apt install ros-foxy-desktop python3-argcomplete
sudo apt install ros-dev-tools
sudo echo "source /opt/ros/foxy/setup.bash" > ~/.bashrc

sudo apt install ros-foxy-control*
sudo apt install ros-foxy-moveit*
sudo apt install ros-foxy-gazebo-ros*
sudo apt install ros-foxy-nav2*

cd ~/benchmark_ws
colcon build --symlink-install
source ./install/setup.bash
