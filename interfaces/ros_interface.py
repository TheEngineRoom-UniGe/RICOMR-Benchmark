import sys
import rospy
import copy
import sys
import numpy as np
from kafka_producer import KafkaProducer
from kafka_admin import KafkaAdmin

from geometry_msgs.msg import Point, Pose
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class UR5Interface:
   def __init__(self, moveit_interface, is_ros=True, ns=""):
      
      self.moveit_interface = moveit_interface

      self.idle_pose = Pose()
      self.idle_pose.position.x = 0.8162378523149748
      self.idle_pose.position.y = 0.19169106600631303
      self.idle_pose.position.z = -0.01222756096174452
      self.idle_pose.orientation.x = -0.003336178036526443
      self.idle_pose.orientation.y = -0.707098688830761
      self.idle_pose.orientation.z = -0.7070978857887898
      self.idle_pose.orientation.w = 0.0035908331833641657
      self.idle_joint_state = [0, 0, 0, 0, 0, 0]

      self.name_space = "/crowd/{0}".format(ns)
      self.trajectory_topic= "robot_{0}_joint_trajectory".format(ns)

      self.is_ros=is_ros

      self.kafka_bootstrap_server='SASL_PLAINTEXT://172.31.35.29:9096,SASL_PLAINTEXT://172.31.35.29:9097,SASL_PLAINTEXT://172.31.35.29:9098'
      self.kafka_key='theengineroom'
      self.kafka_secret='1tYdZP43t20'

      if not(self.is_ros):
         self.kafka_producer = KafkaProducer(bootstrap_serv=self.kafka_bootstrap_server,api_key=self.kafka_key,api_secret=self.kafka_secret)
         self.kafka_admin = KafkaAdmin(bootstrap_serv=self.kafka_bootstrap_server,api_key=self.kafka_key,api_secret=self.kafka_secret)
         self.kafka_admin.create_topic(self.trajectory_topic)

   def home_routine(self):
        
      joint_trajectory_msg = JointTrajectory()
      joint_names = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
      joint_trajectory_msg.joint_names = joint_names

      point = JointTrajectoryPoint()
      point.positions = [0.0] * 6
      joint_trajectory_msg.points.append(point)

      point = JointTrajectoryPoint()
      point.positions = self.idle_joint_state
      joint_trajectory_msg.points.append(point)

      return joint_trajectory_msg
   
   def main_routine(self):
      reach_pose = copy.deepcopy(self.idle_pose)
      z = np.random.uniform(-0.8, 0.8, 1)
      phi = np.random.uniform(-np.pi, np.pi, 1)
      rxy = np.sqrt(1 - z**2)
      x = rxy * np.cos(phi)
      y = rxy * np.sin(phi)
      reach_pose.position.x = float("{:.2f}".format(x[0]))
      reach_pose.position.y = float("{:.2f}".format(y[0]))
      reach_pose.position.z = float("{:.2f}".format(z[0]))

      print("{0}:{1}:{2}".format(x,y,z))

      plan, fraction = self.moveit_interface.plan_cartesian_path(self.moveit_interface.get_joint_state(), reach_pose)
      # Make sure plan is valid..
      if len(plan.joint_trajectory.points) > 2:
        if self.is_ros:
           self.moveit_interface.ros_execute_plan(plan.joint_trajectory)
        else:
           self.kafka_producer.produce_record(topic=self.trajectory_topic,msg=plan.joint_trajectory)

      else:
         plan, fraction = self.moveit_interface.plan_cartesian_path(self.moveit_interface.get_joint_state(), self.idle_pose)
         if len(plan.joint_trajectory.points) > 2:
            if self.is_ros:
               self.moveit_interface.ros_execute_plan(plan.joint_trajectory)
            else:
               self.kafka_producer.produce_record(topic=self.trajectory_topic,msg=plan.joint_trajectory)
      rospy.sleep(3.0)
      # Move back to idle pose
      plan, fraction = self.moveit_interface.plan_cartesian_path(self.moveit_interface.get_joint_state(), self.idle_pose)
      if len(plan.joint_trajectory.points) > 2:
        if self.is_ros:
           self.moveit_interface.ros_execute_plan(plan.joint_trajectory)
        else:
           self.kafka_producer.produce_record(topic=self.trajectory_topic,msg=plan.joint_trajectory)
      rospy.sleep(3.0)
