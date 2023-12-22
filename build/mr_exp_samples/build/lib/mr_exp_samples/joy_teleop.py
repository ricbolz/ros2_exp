import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class JoyTeleop(Node):
    def __init__(self):
        super().__init__('joy_teleop')
        self.subscription = self.create_subscription(
            Joy, 
            'joy',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(
            Twist,
            'cmd_vel', 
            10)
        timer_period = 0.1
        self.timer = self.create_timer(
            timer_period, 
            self.timer_callback)
        self.twist_msg = Twist()
    
    def listener_callback(self, msg):
        #self.get_logger().info('Recieved:"%s, %s"' % (msg.axes, msg.buttons))
        self.twist_msg.linear.x = 0.05 * msg.axes[1]
        self.twist_msg.angular.z = 0.5 * msg.axes[0]
        
    def timer_callback(self):
        self.publisher.publish(self.twist_msg)
        #self.get_logger().info('Publishing:"%s"' % self.twist_msg)

def main():
    rclpy.init()
    node = JoyTeleop()
    rclpy.spin(node)
    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ =="__main__":
    main()