#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ROS_WS="${ROS_WS:-$(cd "${REPO_DIR}/../.." && pwd)}"
ROS_DISTRO="${ROS_DISTRO:-jazzy}"

source "/opt/ros/${ROS_DISTRO}/setup.bash"
source "${ROS_WS}/install/setup.bash"

exec ros2 launch silverhand_system_bringup silverhand_system_arm_hand_moveit.launch.py \
  use_mock_hardware:=false \
  use_rviz:="${SILVERHAND_USE_RVIZ:-false}" \
  arm_can_iface:="${SILVERHAND_ARM_CAN_IFACE:-can0}" \
  arm_node_id:="${SILVERHAND_ARM_NODE_ID:-100}" \
  hand_can_iface:="${SILVERHAND_HAND_CAN_IFACE:-can0}" \
  hand_node_id:="${SILVERHAND_HAND_NODE_ID:-120}"
