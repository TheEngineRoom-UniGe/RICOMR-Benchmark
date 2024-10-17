#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from robot_benchmark.msg import CustomHeader
from std_msgs.msg import Header

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher_ = self.create_publisher(CustomHeader, 'chatter', 100)
        self.timer = self.create_timer(0.002, self.timer_callback)  # 500Hz
        self.seq = 0

    def timer_callback(self):
        msg = CustomHeader()
        msg.stamp = self.get_clock().now().to_msg()
        msg.frame_id = ''
        msg.seq = 0
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    talker = Talker()

    try:
        rclpy.spin(talker)
    except KeyboardInterrupt:
        pass
    finally:
        talker.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
