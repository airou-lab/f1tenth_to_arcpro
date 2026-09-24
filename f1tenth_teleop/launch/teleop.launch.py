import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    joy_dev = LaunchConfiguration('joy_dev')

    pkg_share = get_package_share_directory('f1tenth_teleop')
    teleop_yaml = os.path.join(pkg_share, 'config', 'teleop_twist_joy.yaml')

    # Resolve twist_to_ackermann executable (installed binary or script)
    tta_candidates = [
        os.path.join(os.path.dirname(os.path.dirname(pkg_share)), 'lib', 'f1tenth_teleop', 'twist_to_ackermann'),
        os.path.expanduser('~/arcpro_system/scripts/twist_to_ackermann.py'),
        os.path.expanduser('~/example_scripts/config/twist_to_ackermann.py'),
        os.path.join(pkg_share, '..', '..', '..', 'scripts', 'twist_to_ackermann.py'),
    ]
    tta_path = None
    for cand in tta_candidates:
        cand_norm = os.path.normpath(cand)
        if os.path.isfile(cand_norm) and os.access(cand_norm, os.X_OK):
            tta_path = cand_norm
            break

    actions = [
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
    ]

    # Twist -> Ackermann: /cmd_vel -> /ackermann_cmd
    if tta_path:
        actions.append(
            Node(
                executable=tta_path,
                name='twist_to_ack',
                output='screen',
                parameters=[teleop_yaml, {'use_sim_time': use_sim_time}],
            )
        )
    else:
        actions.append(
            Node(
                package='f1tenth_teleop',
                executable='twist_to_ackermann',
                name='twist_to_ack',
                output='screen',
                parameters=[teleop_yaml, {'use_sim_time': use_sim_time}],
            )
        )

    return LaunchDescription(actions)