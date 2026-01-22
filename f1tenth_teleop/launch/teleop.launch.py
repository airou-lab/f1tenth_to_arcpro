import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    joy_dev = LaunchConfiguration('joy_dev')

    teleop_yaml = os.path.join(
        get_package_share_directory('f1tenth_teleop'),
        'config', 'teleop_twist_joy.yaml'
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('joy_dev', default_value='/dev/input/js0'),

        # Joystick
        Node(
            package='joy', executable='joy_node', name='joy', output='screen',
            parameters=[{'device': joy_dev, 'deadzone': 0.05,
                         'autorepeat_rate': 20.0, 'use_sim_time': use_sim_time}]
        ),

        # teleop_twist_joy -> /cmd_vel (uses the YAML from f1tenth_teleop)
        Node(
            package='teleop_twist_joy', executable='teleop_node',
            name='teleop', output='screen',
            parameters=[teleop_yaml, {'use_sim_time': use_sim_time}]
        ),

        # Twist → Ackermann: /cmd_vel → /ackermann_cmd (reads "twist_to_ack" section)
        # Node(
        #     package='f1tenth_teleop', executable='twist_to_ackermann',
        #     name='twist_to_ack', output='screen',
        #     parameters=[teleop_yaml, {'use_sim_time': use_sim_time}],
        # ),
    ])