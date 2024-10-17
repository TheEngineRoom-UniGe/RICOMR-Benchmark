cmake_minimum_required(VERSION 3.5)
project(robot_benchmark)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CustomHeader.msg"
  DEPENDENCIES builtin_interfaces
)

include_directories(include)
link_directories(
  ${gazebo_dev_LIBRARY_DIRS}
)

set(THIS_PACKAGE_INCLUDE_DEPENDS
  rclcpp
  std_msgs
)

install(DIRECTORY launch config urdf DESTINATION share/${PROJECT_NAME})

ament_package()
