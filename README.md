# Directory Tree
```bash
.
├── ROS2
│   ├── bootstrap.sh
│   ├── cyclone_profile.xml
│   ├── readme.txt
│   └── src
│       └── robot_benchmark
│           ├── CMakeLists.txt
│           ├── config
│           │   └── ur
│           │       └── ur5
│           │           ├── chomp_planning.yaml
│           │           ├── default_kinematics.yaml
│           │           ├── initial_positions.yaml
│           │           ├── joint_limits.yaml
│           │           ├── joint_limits_planning.yaml
│           │           ├── kinematics.yaml
│           │           ├── moveit_controller_manager.yaml
│           │           ├── ompl_planning.yaml
│           │           ├── physical_parameters.yaml
│           │           ├── robot.srdf
│           │           ├── ros_controllers_robot.yaml
│           │           └── visual_parameters.yaml
│           ├── launch
│           │   ├── automate.py
│           │   ├── dep
│           │   │   ├── moveit2_interface.py
│           │   │   └── ur5.py
│           │   ├── echoer_ros2.py
│           │   ├── gazebo_launch_empty_world.launch.py
│           │   ├── gazebo_spawn_robots.launch.py
│           │   ├── latency_ros2.py
│           │   ├── moveit2_planner.py
│           │   ├── publisher_ros2.py
│           │   └── subscribers
│           ├── msg
│           │   └── CustomHeader.msg
│           ├── package.xml
│           └── urdf
│               └── ur
│                   ├── inc
│                   │   ├── ur_common.xacro
│                   │   └── ur_transmissions.xacro
│                   ├── meshes
│                   │   └── ur5
│                   │       ├── collision
│                   │       │   ├── base.stl
│                   │       │   ├── forearm.stl
│                   │       │   ├── shoulder.stl
│                   │       │   ├── upperarm.stl
│                   │       │   ├── wrist1.stl
│                   │       │   ├── wrist2.stl
│                   │       │   └── wrist3.stl
│                   │       └── visual
│                   │           ├── base.dae
│                   │           ├── forearm.dae
│                   │           ├── shoulder.dae
│                   │           ├── upperarm.dae
│                   │           ├── wrist1.dae
│                   │           ├── wrist2.dae
│                   │           └── wrist3.dae
│                   └── ur5
│                       ├── ur_macro.xacro
│                       ├── ur_ros2_control.xacro
│                       └── ur_urdf.xacro
├── bootstrap.sh
├── echoer.py
├── echoer_kafka.py
├── frequency.py
├── init_ros_sim.py
├── interfaces
│   ├── kafka_admin.py
│   ├── kafka_producer.py
│   ├── moveit_interface.py
│   ├── planning_execution.py
│   └── ros_interface.py
├── latency.py # Calculate latency for ROS-Gazebo
├── latency_kafka.py # calculate latency for Kafka-RICO
├── moveit_crowd.launch # Launch simulation and spawn n UR5 robots
├── moveit_planning_execution.launch # UR5 plan to a random point in the space
├── publisher.py
├── publisher_kafka.py
├── requirements.yml
├── rviz.rviz
├── spawn_controllers.py
├── start_kafka_simulation.sh
├── start_ros_control.sh
├── start_ros_sim.sh
├── subscriber.py
├── throughput.py # calculate msg throughput versus subscribers
├── top.sh #Run on host to collect top processes & VM metrics
├── topic_echo.py #Echo all the MSGs published to a certain topic
├── topic_subs_kafka.py #Kafka msg consumer
├── topic_subscribers.py #ROS msg consumer
└── ur5_crowd_bringup.launch #spawn one UR5 robot
```
# Workspace Setup ROS1

On Ubuntu 20.04 execute:
```bash
sudo apt-get update
sudo apt-get upgrade
sudo ./bootstrap.sh
```
# Running The Simulation
The simulation is divided over a host virtual machine and many workers. The host is supposed to be GPU accelerated workers requires no specific hardware.
X86 is the only supported and benchmarked CPU architecture. Follow the previous section to setup both the host and workers.
```bash
sudo ./start_kafka_simulation.sh #Host VM Running Kafka-RICO simulation
sudo ./start_ros_sim.sh #Host VM running ROS-Gazebo simulation
sudo ./start_ros_control.sh #Workers, each worker spawn and control one UR5 robot
```
