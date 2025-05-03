import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions      import Command
from launch_ros.actions       import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg = get_package_share_directory('dofbot_description')
    xacro_file = os.path.join(pkg, 'urdf', 'dofbot.urdf.xacro')
    urdf_path  = xacro_file
    cfg_file   = os.path.join(pkg, 'config', 'controllers.yaml')

    # Expand xacro
    robot_description_content = Command([
        'xacro ', xacro_file,
        ' prefix:=', ''
    ])

    # 1) Launch Ignition (GZ Fortress)
    gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch', 'gz_sim.launch.py'
            )
        ),
        launch_arguments={'gz_args': ''}.items()
    )

    # 2) Publish robot_description
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'robot_description': robot_description_content
        }]
    )

    # 3) ros2_control manager
    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        name='controller_manager',
        output='screen',
        parameters=[cfg_file],     # your controllers.yaml only
        remappings=[('/robot_description', 'robot_description')],
        # or if you prefer explicit param:
        # parameters=[{'robot_description': robot_description_content}, cfg_file],
    )


    # 4) Spawn into Ignition
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'dofbot', '-topic', 'robot_description'],
        output='screen'
    )

    # 5) Autospawn controllers
    load_jsb = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen'
    )
    load_ptc = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['position_trajectory_controller', '--controller-manager', '/controller_manager'],
        output='screen'
    )

    # 6) Optional GUI sliders
    jsp_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

    return LaunchDescription([
        gz,
        rsp,
        control_node,
        spawn_entity,
        load_jsb,
        load_ptc,
        jsp_gui,
    ])