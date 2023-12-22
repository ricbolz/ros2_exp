import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class HelloPublisher(Node):
    def __init__(self):
        super().__init__('hello_publisher')
        self.publisher = self.create_publisher(String, 'hello_topic', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0

    def timer_callback(self) :
        msg =String()
        msg.data = 'Hello World(%d)' % self.count
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"'% msg.data)
        self.count+=1



def main():
    rclpy.init()

    node = HelloPublisher()

    rclpy.spin(node)

    rclpy.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()