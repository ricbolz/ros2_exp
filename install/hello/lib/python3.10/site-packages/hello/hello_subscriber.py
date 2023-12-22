import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from raspimouse_msgs.msg import LightSensors

class HelloSubscriber(Node):
    def __init__(self):
        super().__init__('hello_subscriber')
        self.subscription= self.create_subscription(
            String,
            'hello_topic',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg) :
        self.get_logger().info('Received: "%s"' % msg.data)




def main():
    rclpy.init()

    node = HelloSubscriber()

    rclpy.spin(node)

    rclpy.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()