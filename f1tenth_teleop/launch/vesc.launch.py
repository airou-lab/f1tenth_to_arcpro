import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def cfg(name):
    share = get_package_share_directory('launches')
    return os.path.join(share, 'config', name)

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    vesc_port    = LaunchConfiguration('vesc_port')
    vesc_baud    = LaunchConfiguration('vesc_baud')
    base_frame   = LaunchConfiguration('base_frame')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('vesc_port',    default_value='/dev/ttyACM0'),
        DeclareLaunchArgument('vesc_baud',    default_value='115200'),
        DeclareLaunchArgument('base_frame',   default_value='base_link'),

        # 1) ackermann_mux (YAML only)
        #Node(
        #    package='ackermann_mux', executable='ackermann_mux',
        #    name='ackermann_mux', output='screen',
        #    parameters=[cfg('ackermann_mux_topics.yaml'),
        #                cfg('ackermann_mux_locks.yaml')]
        #),

        # 2) Ackermann -> VESC (YAML only), subscribe to mux output 'cmd_muxed'
        Node(
            package='vesc_ackermann', executable='ackermann_to_vesc_node',
            name='ackermann_to_vesc_node', output='screen',
            remappings=[('cmd', 'ackermann_cmd')],
            parameters=[cfg('ack2vesc.yaml')]
        ),

        # 3) VESC driver (YAML + fixed defaults; CLI override still possible if ever needed)
        Node(
            package='vesc_driver', executable='vesc_driver_node',
            name='vesc_driver', output='screen',
            parameters=[cfg('vesc_driver.yaml'),
                        {'port': vesc_port,
                         'baud': vesc_baud,
                         'interface': 'serial',
                         'frame_id': base_frame,
                         'use_sim_time': use_sim_time}]
        ),
    ])
