import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from raspimouse_msgs.msg import LightSensors, Switches, Leds
from std_srvs.srv import SetBool
from std_msgs.msg import String

class RobotNode(Node):
    def __init__(self):
        super().__init__('robot_node')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10)
        self.switch_sub = self.create_subscription(
            Switches,
            'switches',
            self.switch_callback,
            10)
        self.light_pub = self.create_publisher(
            Leds,
            'leds',
            10)
        self.publisher = self.create_publisher(String, 'hello_topic', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0
        
        self.velocity = 0.0

    def timer_callback(self) :
        msg =String()
        msg.data = 'Hello World(%d)' % self.count
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"'% msg.data)
        self.count+=1

    def listener_callback(self, msg):
        twist = Twist()

        # For a PS2 controller, the left stick's x-axis (usually msg.axes[0]) controls the direction
        twist.angular.z = msg.axes[0] 

        # Check if the 'X' button (usually msg.buttons[2] for a PS2 controller) is pressed
        if msg.buttons[2] == 1:
            self.velocity += 0.01  # Increase the velocity
            if self.velocity > 0.2 :
                self.velocity = 0.2
            self.get_logger().info('The "X" button is pressed. Increasing velocity.')

        # Check if the 'Square' button (usually msg.buttons[3] for a PS2 controller) is pressed
        elif msg.buttons[3] == 1:
            self.velocity -= 0.01  # Decrease the velocity (act as brake)
            if self.velocity < -0.2 :
                self.velocity = -0.2
            self.get_logger().info('The "Square" button is pressed. Decreasing velocity.')
        else :
            self.velocity = 0.0
        # Apply the velocity
        twist.linear.x = self.velocity

        self.publisher.publish(twist)
        self.get_logger().info('Publishing Twist: linear.x=%f, angular.z=%f' % (twist.linear.x, twist.angular.z))

    def switch_callback(self, msg):
        leds = Leds()
        if msg.switch0:
            leds.left_side = Leds.LED_ON
        else:
            leds.left_side = Leds.LED_OFF
        if msg.switch1:
            leds.right_side = Leds.LED_ON
        else:
            leds.right_side = Leds.LED_OFF
        self.light_pub.publish(leds)
        self.get_logger().info('Publishing Leds: left_side=%d, right_side=%d' % (leds.left_side, leds.right_side))

def main():
    rclpy.init()
    node = RobotNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ =="__main__":
    main()