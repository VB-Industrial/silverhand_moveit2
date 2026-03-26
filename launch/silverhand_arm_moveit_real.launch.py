from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    can_iface = LaunchConfiguration("can_iface")
    node_id = LaunchConfiguration("node_id")

    launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("silverhand_moveit2"), "launch", "silverhand_arm_moveit_common.launch.py"]
            )
        ),
        launch_arguments={
            "use_rviz": "false",
            "use_mock_hardware": "false",
            "can_iface": can_iface,
            "node_id": node_id,
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("can_iface", default_value="can0"),
            DeclareLaunchArgument("node_id", default_value="100"),
            launch,
        ]
    )
