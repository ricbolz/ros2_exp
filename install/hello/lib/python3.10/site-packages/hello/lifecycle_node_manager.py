import rclpy
from rclpy.node import Node
from lifecycle_msgs.msg import State, Transition
from lifecycle_msgs.srv import ChangeState, GetState
import time


class Manager(Node):

    def __init__(self):
        super().__init__('lifecycle_node_manager')
        self.components = self.get_parameter('components').get_parameter_value().string_array_value
        if not self.components:
            self.get_logger().error("param 'components' has no value.")
            rclpy.shutdown()

    def get_node_state(self, target_node_name, time_out=10):
        request = GetState.Request()
        service_name = target_node_name + '/get_state'
        client = self.create_client(GetState, service_name)

        if not client.wait_for_service(time_out):
            self.get_logger().error("Service %s is not available.", service_name)
            return State.PRIMARY_STATE_UNKNOWN

        future_result = client.call_async(request)
        rclpy.spin_until_future_complete(self, future_result, timeout_sec=time_out)

        if future_result.result() is None:
            self.get_logger().error("Service %s timed out while getting current state.", service_name)
            return State.PRIMARY_STATE_UNKNOWN

        return future_result.result().current_state.id

    def change_node_state(self, target_node_name, transition, time_out=10):
        request = ChangeState.Request()
        request.transition.id = transition

        service_name = target_node_name + '/change_state'
        client = self.create_client(ChangeState, service_name)

        if not client.wait_for_service(time_out):
            self.get_logger().error("Service %s is not available.", service_name)
            return False

        future_result = client.call_async(request)
        rclpy.spin_until_future_complete(self, future_result, timeout_sec=time_out)

        if future_result.result() is None:
            self.get_logger().error("Service %s timed out while changing current state.", service_name)
            return False

        return future_result.result().success

    def all_nodes_are_unconfigured(self):
        return all(self.get_node_state(s) == State.PRIMARY_STATE_UNCONFIGURED for s in self.components)

    def all_nodes_are_inactive(self):
        return all(self.get_node_state(s) == State.PRIMARY_STATE_INACTIVE for s in self.components)

    def all_nodes_are_active(self):
        return all(self.get_node_state(s) == State.PRIMARY_STATE_ACTIVE for s in self.components)

    def configure_all_nodes(self):
        return all(self.change_node_state(s, Transition.TRANSITION_CONFIGURE) for s in self.components)

    def activate_all_nodes(self):
        return all(self.change_node_state(s, Transition.TRANSITION_ACTIVATE) for s in self.components)

    def run(self):
        if not self.all_nodes_are_unconfigured():
            self.get_logger().error("Failed to launch nodes.")
            rclpy.shutdown()
            return

        self.get_logger().info("Launched all nodes.")

        if not self.configure_all_nodes():
            self.get_logger().error("Failed to configure nodes.")
            rclpy.shutdown()
            return

        self.get_logger().info("Configured all nodes.")

        if not self.activate_all_nodes():
            self.get_logger().error("Failed to activate nodes.")
            rclpy.shutdown()
            return

        self.get_logger().info("Activated all nodes.")

        while rclpy.ok():
            time.sleep(10)
            if self.all_nodes_are_active():
                self.get_logger().info("All nodes are active.")
            else:
                self.get_logger().error("Any node is not active.")

        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    manager = Manager()

    if not manager.all_nodes_are_unconfigured():
        manager.get_logger().error("Failed to launch nodes.")
        rclpy.shutdown()
        return

    manager.get_logger().info("Launched all nodes.")

    if not manager.configure_all_nodes():
        manager.get_logger().error("Failed to configure nodes.")
        rclpy.shutdown()
        return

    manager.get_logger().info("Configured all nodes.")

    if not manager.activate_all_nodes():
        manager.get_logger().error("Failed to activate nodes.")
        rclpy.shutdown()
        return

    manager.get_logger().info("Activated all nodes.")

    while rclpy.ok():
        time.sleep(10)
        if manager.all_nodes_are_active():
            manager.get_logger().info("All nodes are active.")
        else:
            manager.get_logger().error("Any node is not active.")

    rclpy.shutdown()


if __name__ == '__main__':
    main()
