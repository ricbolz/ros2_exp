import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from raspimouse_msgs.msg import LightSensors, Switches, Leds
from std_srvs.srv import SetBool

class JoypadMouseController(Node):
    def __init__(self):
        super().__init__('joypad_mouse_controller')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10)
      
        self.velocity = 0.0

    def listener_callback(self, msg):
        twist = Twist()

        # For a PS2 controller, the left stick's x-axis (usually msg.axes[0]) controls the direction
        twist.angular.z = msg.axes[0] 

        # Check if the 'X' button (usually msg.buttons[2] for a PS2 controller) is pressed
        if msg.buttons[2] == 1:
            self.velocity += 0.005  # Increase the velocity
            if self.velocity > 0.1 :
                self.velocity = 0.1
            self.get_logger().info('The "X" button is pressed. Increasing velocity.')

        # Check if the 'Square' button (usually msg.buttons[3] for a PS2 controller) is pressed
        elif msg.buttons[3] == 1:
            self.velocity -= 0.005  # Decrease the velocity (act as brake)
            if self.velocity < -0.1 :
                self.velocity = -0.1
            self.get_logger().info('The "Square" button is pressed. Decreasing velocity.')
        else :
            self.velocity = 0.0
        # Apply the velocity
        twist.linear.x = self.velocity

        self.publisher.publish(twist)
        self.get_logger().info('Publishing Twist: linear.x=%f, angular.z=%f' % (twist.linear.x, twist.angular.z))

   

def main():
    rclpy.init()
    node = JoypadMouseController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ =="__main__":
    main()