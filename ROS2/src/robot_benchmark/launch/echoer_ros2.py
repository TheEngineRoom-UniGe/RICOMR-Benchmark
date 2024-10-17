#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from robot_benchmark.msg import CustomHeader
import threading

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.publisher_ = self.create_publisher(CustomHeader, 'chatter', 10)  # Publisher
        self.subscription = self.create_subscription(
            CustomHeader, 'chatter', self.callback,10)  # Subscriber
        self.subscription  # prevent unused variable warning

    def callback(self, msg):
        # Check if seq == 1, if so return without republishing
        if msg.seq == 1:
            return

        # Modify the sequence and republish the message
        msg.seq = 1
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    listener = Listener()

    try:
        rclpy.spin(listener)  # Keep the node alive
    except KeyboardInterrupt:
        pass
    finally:
        listener.destroy_node()
        rclpy.shutdown()  # Shut down ROS2

if __name__ == '__main__':
    main()

