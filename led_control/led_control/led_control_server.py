#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from led_interfaces.srv import ActivateLED
from gpiozero import LED

# GPIO pin numbers (BCM numbering) - adjust to match your wiring
LED_PINS = [17, 27, 22]

class LEDServerNode(Node):
    def __init__(self):
        super().__init__('led_server')

        # Initialize LEDs
        self.leds = [LED(pin) for pin in LED_PINS]
        self.get_logger().info(f"Initialized LEDs on GPIO pins: {LED_PINS}")

        self.led_activate_service_ = self.create_service(ActivateLED, "activate_led", self.callback_activate_led)
        self.get_logger().info("LED Server has been started!")

    def callback_activate_led(self, request: ActivateLED.Request, response: ActivateLED.Response):
        led_status = request.led_arr_status

        for i, (led, status) in enumerate(zip(self.leds, led_status)):
            if status:
                led.on()
            else:
                led.off()
            self.get_logger().info(f"LED{i+1} (GPIO {LED_PINS[i]}): {'ON' if status else 'OFF'}")

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