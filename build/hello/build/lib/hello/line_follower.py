import rclpy
from rclpy.executors import MultiThreadedExecutor
from raspimouse.raspimouse_component import Raspimouse
from raspimouse_ros2_examples.line_follower_component import Follower

def main():
    rclpy.init()
    executor = MultiThreadedExecutor()

    raspimouse = Raspimouse()
    line_follower = Follower()

    executor.add_node(raspimouse.get_node_base_interface())
    executor.add_node(line_follower.get_node_base_interface())

    executor.spin()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
