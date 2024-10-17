#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from robot_benchmark.msg import CustomHeader  # Import your custom message
import threading
import time

average = 0.0
counter = 0
counter_throughput = 0.0


class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            CustomHeader, 'chatter', self.callback, 10)
        self.subscription  # prevent unused variable warning

        # Start throughput logging in a separate thread
        self.msg_throughput()
    
    def callback(self, msg):
        global average, counter, counter_throughput
        
        if msg.seq == 0:
            return

        receive_time = self.get_clock().now().nanoseconds
        send_time = msg.stamp.sec * 1e9 + msg.stamp.nanosec  # Convert ROS2 Time to nanoseconds
        
        # Calculate the latency
        latency = receive_time - send_time
        counter += 1
        average += latency
        counter_throughput += 1

        # Write latency to file every 10 messages
        if counter % 10 == 0:
            with open("latency.csv", "a") as file_latency:
                file_latency.write(f"{latency},\n")

        # Log average latency every 500 messages
        if counter >= 500:
            self.get_logger().info(f"Average latency over 500 messages: {average / 500.0} ns")
            counter = 0
            average = 0

    def msg_throughput(self):
        global counter_throughput
        
        # Log and write message throughput every second
        self.get_logger().info(f"Messages delivered: {counter_throughput}")
        with open("delivered.csv", "a") as file_msg:
            file_msg.write(f"{counter_throughput},\n")
        
        counter_throughput = 0
        threading.Timer(1, self.msg_throughput).start()  # Repeat every second


def main(args=None):
    rclpy.init(args=args)
    listener = Listener()

    try:
        rclpy.spin(listener)  # Keep the node alive
    except KeyboardInterrupt:
        pass
    finally:
        listener.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

