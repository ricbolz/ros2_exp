import rclpy
from rclpy.node import Node

class PrintHello(Node):
    def __init__(self):
        super().__init__('print_hello')
        print('Hello World')


def main():
    rclpy.init()

    node = PrintHello()

    rclpy.spin(node)

    rclpy.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()