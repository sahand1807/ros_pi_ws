#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from led_interfaces.srv import ActivateLED

class LEDClientNode(Node):
    def __init__(self):
        super().__init__('led_client')
        self.client_ = self.create_client(ActivateLED, "activate_led")  


    def call_led_server(self, value):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().info("Waiting for service...")
        request = ActivateLED.Request()
        request.led_arr_status = value
        future = self.client_.call_async(request)
        future.add_done_callback(self.callback_led_activate_response)

    def callback_led_activate_response(self, future):
        response = future.result()
        self.get_logger().info("Success flag: " + str(response.success))



def main(args=None):
    rclpy.init(args=args) # initialize ros2 communications
    node = LEDClientNode() # initialize the node
    node.call_led_server([0, 0, 0]) 
    rclpy.spin(node) # we block the execution here, the program stays alive, and thus the node!
    rclpy.shutdown() # after the node is killed with ctrl+c shut down ros2


# allow running the program without using colcon to build it
if __name__ == "__main__":
    main()