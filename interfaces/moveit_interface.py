import sys
import rospy
import moveit_commander


from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from moveit_msgs.msg import RobotState, DisplayTrajectory


class moveitInterface:
  
  def __init__(self,ns=""):

    self.namespace = "/crowd/{0}".format(ns)
    
    joint_state_topic = ['joint_states:={0}/joint_states'.format(self.namespace)]
    moveit_commander.roscpp_initialize(joint_state_topic)
    rospy.init_node('ur5_moveit_node', anonymous=True)

    robot = moveit_commander.RobotCommander(robot_description="{0}/robot_description".format(self.namespace))
    scene = moveit_commander.PlanningSceneInterface(ns=self.namespace)
    group_name = "manipulator"
    group = moveit_commander.MoveGroupCommander(name=group_name, robot_description="{0}/robot_description".format(self.namespace), ns=self.namespace)
    
    ## We create a `DisplayTrajectory`_ publisher which is used later to publishtrajectories for RViz to visualize:
    display_trajectory_publisher = rospy.Publisher('{0}/move_group/display_planned_path'.format(self.namespace),DisplayTrajectory, queue_size=20)

    planning_frame = group.get_planning_frame()
    eef_link = group.get_end_effector_link()
    group_names = robot.get_group_names()
  
    # Misc variables
    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.group = group
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.eef_link = eef_link
    self.group_names = group_names


    rospy.sleep(2.0)
    self.add_ground_plane()

  def get_ee_pose(self):
    return self.group.get_current_pose().pose
  
  def add_ground_plane(self):
    p = PoseStamped()
    p.header.frame_id = self.robot.get_planning_frame()
    p.pose.position.x = 0.0
    p.pose.position.y = 0.0
    p.pose.position.z = -0.2
    p.pose.orientation.x = 0.0
    p.pose.orientation.y = 0.0
    p.pose.orientation.z = 0.0
    p.pose.orientation.w = 0.0

    self.scene.add_plane("ground", p)
  
  def get_current_state(self):
    return self.robot.get_current_state()
  
  def get_joint_state(self):
    return self.group.get_current_joint_values()

  def set_gripper_state(self, new_state):
    joint_trajectory_msg = JointTrajectory()
    joint_names = ["gripper_base_gripper_left_joint", "gripper_joint"]
    joint_trajectory_msg.joint_names = joint_names

    point = JointTrajectoryPoint()
    point.positions = [-0.04, 0.08] if new_state == 0 else [-0.02, 0.055]
    joint_trajectory_msg.points.append(point)

    point = JointTrajectoryPoint()
    point.positions = [-0.04, 0.08] if new_state == 1 else [-0.02, 0.055]
    joint_trajectory_msg.points.append(point)

    return joint_trajectory_msg
  
  def get_robot_state(self, starting_joint_config):

    js = JointState()
    js.header.stamp = rospy.Time.now()
    js.name = self.group.get_joints()[1:-2]
    js.position = starting_joint_config

    moveit_robot_state = RobotState()
    moveit_robot_state.joint_state = js

    return moveit_robot_state
  
  def plan_joint_state(self, starting_joint_config, target_joint_config):
    
    self.group.set_start_state(self.get_robot_state(starting_joint_config))
    return self.group.plan(joints = target_joint_config)

  def plan_cartesian_path(self, starting_joint_config, target_pose):

    self.group.set_start_state(self.get_robot_state(starting_joint_config))

    waypoints = []
    waypoints.append(target_pose)
    
    (plan, fraction) = self.group.compute_cartesian_path(waypoints, 0.01, 0.0)        
    # Note: We are just planning, not asking move_group to actually move the robot yet:
    return plan, fraction
  

  def ros_execute_plan(self, plan):

    self.group.execute(plan, wait=True)