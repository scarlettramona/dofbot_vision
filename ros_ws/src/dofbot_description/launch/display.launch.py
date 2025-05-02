#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('dofbot_description')

    # allow overriding the xacro and rviz files on the command-line
    urdf_file = LaunchConfiguration('urdf_file',
                    default=os.path.join(pkg_share, 'urdf', 'dofbot.urdf.xacro'))
    rviz_config = LaunchConfiguration('rviz_config',
                    default=os.path.join(pkg_share, 'rviz', 'dofbot_humble.rviz'))

    # process the xacro into a robot_description parameter
    robot_description = {'robot_description':
        Command(['xacro ', urdf_file])}

    return LaunchDescription([
        # allow passing alternatives if you like
        DeclareLaunchArgument('urdf_file', default_value=urdf_file),
        DeclareLaunchArgument('rviz_config', default_value=rviz_config),

        # publish joint states
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),

        # publish the robot_description + TF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[robot_description]
        ),

        # open RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config]
        ),
    ])
