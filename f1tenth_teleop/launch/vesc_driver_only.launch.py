import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    vesc_port = LaunchConfiguration('vesc_port')
    vesc_baud = LaunchConfiguration('vesc_baud')
    base_frame = LaunchConfiguration('base_frame')

    vesc_driver_yaml = os.path.join(
        get_package_share_directory('vesc_driver'),
        'config', 'vesc_driver.yaml'
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('vesc_port', default_value='/dev/ttyACM0'),
        DeclareLaunchArgument('vesc_baud', default_value='115200'),
        DeclareLaunchArgument('base_frame', default_value='base_link'),

        Node(
            package='vesc_driver', executable='vesc_driver_node',
            name='vesc_driver', output='screen',
            parameters=[vesc_driver_yaml,
                        {'port': vesc_port, 'baud': vesc_baud,
                         'interface':'serial', 'frame_id': base_frame,
                         'use_sim_time': use_sim_time}]
        ),
    ])
