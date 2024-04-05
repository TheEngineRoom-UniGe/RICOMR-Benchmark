
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_context import LaunchContext
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml

def generate_launch_description():

    
    declare_use_sim_time = DeclareLaunchArgument(
        name="use_sim_time", default_value='true', description="Use simulator time"
    )

    robot_type = "ur5"

    declare_robot_type = DeclareLaunchArgument(
        name="robot_type", default_value=robot_type, description="Robot type"
    )

    gazebo_server = ExecuteProcess(
        cmd=[
            "gzserver",
            "--verbose",
            "-u",
            "-s", "libgazebo_ros_factory.so",
            "-s", "libgazebo_ros_init.so",
        ],
        output="screen",
    )
    gazebo_client = ExecuteProcess(cmd=["gzclient"], output="screen")

    ld = LaunchDescription()
    ld = LaunchDescription()
    ld.add_action(declare_robot_type)
    ld.add_action(declare_use_sim_time)
    ld.add_action(gazebo_server)
    ld.add_action(gazebo_client)

    return ld