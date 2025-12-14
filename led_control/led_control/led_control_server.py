#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from led_interfaces.srv import ActivateLED

class LEDServerNode(Node):
    def __init__(self):
        super().__init__('led_server')
        self.led_activate_service_ = self.create_service(ActivateLED, "activate_led", self.callback_activate_led)
        self.get_logger().info("LED Server has been started!")


    def callback_activate_led(self, request: ActivateLED.Request, response: ActivateLED.Response):
        self.led_status_ = request.led_arr_status
        self.get_logger().info("LED1 set to: " + str(self.led_status_[0])) 
        self.get_logger().info("LED2 set to: " + str(self.led_status_[1])) 
        self.get_logger().info("LED3 set to: " + str(self.led_status_[2])) 
        response.success = True
        return response
    
def main(args=None):
    rclpy.init(args=args) # initialize ros2 communications
    node = LEDServerNode() # initialize the node
    rclpy.spin(node) # we block the execution here, the program stays alive, and thus the node!
    rclpy.shutdown() # after the node is killed with ctrl+c shut down ros2


# allow running the program without using colcon to build it
if __name__ == "__main__":
    main()