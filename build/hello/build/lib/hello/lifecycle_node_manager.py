import rclpy
from rclpy.node import Node
from lifecycle_msgs.msg import State, Transition
from lifecycle_msgs.srv import ChangeState, GetState
import time

def state_of(target_node_name, node, time_out=10):
    request = GetState.Request()
    service_name = target_node_name + '/get_state'
    client = node.create_client(GetState, service_name)

    if not client.wait_for_service(time_out):
        node.get_logger().error("Service %s is not available.", service_name)
        return State.PRIMARY_STATE_UNKNOWN

    future_result = client.call_async(request)
    rclpy.spin_until_future_complete(node, future_result, timeout_sec=time_out)

    if future_result.result() is None:
        node.get_logger().error("Service %s timed out while getting current state.", service_name)
        return State.PRIMARY_STATE_UNKNOWN

    return future_result.result().current_state.id

def all_nodes_are_unconfigured(node, target_node_names):
    return all(state_of(s, node) == State.PRIMARY_STATE_UNCONFIGURED for s in target_node_names)

def all_nodes_are_inactive(node, target_node_names):
    return all(state_of(s, node) == State.PRIMARY_STATE_INACTIVE for s in target_node_names)

def all_nodes_are_active(node, target_node_names):
    return all(state_of(s, node) == State.PRIMARY_STATE_ACTIVE for s in target_node_names)

def change_state(target_node_name, node, transition, time_out=10):
    request = ChangeState.Request()
    request.transition.id = transition

    service_name = target_node_name + '/change_state'
    client = node.create_client(ChangeState, service_name)

    if not client.wait_for_service(time_out):
        node.get_logger().error("Service %s is not available.", service_name)
        return False

    future_result = client.call_async(request)
    rclpy.spin_until_future_complete(node, future_result, timeout_sec=time_out)

    if future_result.result() is None:
        node.get_logger().error("Service %s timed out while changing current state.", service_name)
        return False

    return future_result.result().success

def configure_all_nodes(node, target_node_names):
    return all(change_state(s, node, Transition.TRANSITION_CONFIGURE) for s in target_node_names)

def activate_all_nodes(node, target_node_names):
    return all(change_state(s, node, Transition.TRANSITION_ACTIVATE) for s in target_node_names)

def main(args=None):
    rclpy.init(args=args)

    node = Node('lifecycle_node_manager')

    components = node.get_parameter('components').get_parameter_value().string_array_value
    if not components:
        node.get_logger().error("param 'components' has no value.")
        rclpy.shutdown()
    
    if not all_nodes_are_unconfigured(node, components):
        node.get_logger().error("Failed to launch nodes.")
        rclpy.shutdown()
    else:
        node.get_logger().info("Launched all nodes.")

    if not configure_all_nodes(node, components):
        node.get_logger().error("Failed to configure nodes.")
        rclpy.shutdown()
    else:
        node.get_logger().info("Configured all nodes.")

    if not activate_all_nodes(node, components):
        node.get_logger().error("Failed to activate nodes.")
        rclpy.shutdown()
    else:
        node.get_logger().info("Activated all nodes.")

    while rclpy.ok():
        time.sleep(10)
        if all_nodes_are_active(node, components):
            node.get_logger().info("All nodes are active.")
        else:
            node.get_logger().error("Any node is not active.")
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
