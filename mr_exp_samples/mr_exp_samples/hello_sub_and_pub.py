import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class HelloSubAndPub(Node):
    def __init__(self):
        super().__init__('hello_sub_and_pub')
        self.subscription = self.create_subscription(
            String, 
            'hello_topic1',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(
            String,
            'hello_topic2', 
            10)
        timer_period = 0.5
        self.timer = self.create_timer(
            timer_period, 
            self.timer_callback)
        self.str="Hello"
    
    def listener_callback(self, msg):
        self.get_logger().info('Recieved:"%s"' % msg.data)
        self.str=msg.data

    def timer_callback(self):
        msg=String()
        msg.data=self.str
        self.publisher.publish(msg)
        self.get_logger().info('Publishing:"%s"' % msg.data)

def main():
    rclpy.init()
    node = HelloSubAndPub()
    rclpy.spin(node)
    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ =="__main__":
    main()