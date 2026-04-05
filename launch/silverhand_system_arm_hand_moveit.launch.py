from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_rviz = LaunchConfiguration("use_rviz")
    use_mock_hardware = LaunchConfiguration("use_mock_hardware")
    arm_can_iface = LaunchConfiguration("arm_can_iface")
    arm_node_id = LaunchConfiguration("arm_node_id")
    hand_can_iface = LaunchConfiguration("hand_can_iface")
    hand_node_id = LaunchConfiguration("hand_node_id")
    rviz_config = LaunchConfiguration("rviz_config")

    launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("silverhand_system_bringup"), "launch", "silverhand_system_common.launch.py"]
            )
        ),
        launch_arguments={
            "use_rviz": use_rviz,
            "run_robot_bringup": "true",
            "run_move_group": "true",
            "use_mock_hardware": use_mock_hardware,
            "arm_can_iface": arm_can_iface,
            "arm_node_id": arm_node_id,
            "hand_can_iface": hand_can_iface,
            "hand_node_id": hand_node_id,
            "rviz_config": rviz_config,
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("use_rviz", default_value="true"),
            DeclareLaunchArgument("use_mock_hardware", default_value="true"),
            DeclareLaunchArgument("arm_can_iface", default_value="can0"),
            DeclareLaunchArgument("arm_node_id", default_value="100"),
            DeclareLaunchArgument("hand_can_iface", default_value="can0"),
            DeclareLaunchArgument("hand_node_id", default_value="120"),
            DeclareLaunchArgument(
                "rviz_config",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("silverhand_system_bringup"), "config", "moveit.rviz"]
                ),
            ),
            launch,
        ]
    )
