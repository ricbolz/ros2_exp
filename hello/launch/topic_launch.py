from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hello',
            namespace='hello',
            executable='hello_publisher',
        ),
        Node(
            package='hello',
            namespace='hello',
            executable='hello_subscriber',
        ),
        Node(
            package='hello',
            namespace='hello',
            executable='joypad_mouse_controller',
        ),
        Node(
            package='hello',   
            namespace='hello',
            executable='lightsensor_monitor',
        ),
        Node(
            package='hello',
            namespace='hello',
            executable='line_follower_component',
        )
    ])