fastdds discovery --server-id 0
ros2 launch robot_benchmark gazebo_launch_empty_world.launch.py
ros2 launch robot_benchmark gazebo_spawn_robots.launch.py robots_nb:=7
#python3 moveit2_planner.py --ros-args -r __ns:=/benchmark/ur5_1 -p position:="[0.5, 0.4,0.2]" -p cartesian:=True
python3 ~/RICOMR-Benchmark/ROS2/src/robot_benchmark/launch/automate.py --namespace=/benchmark/ur5_0 
