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
        self.velocity = 0.1* msg.axes[2]

 
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