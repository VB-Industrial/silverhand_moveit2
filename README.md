# silverhand_system_bringup

Upper-level bringup package for the SilverHand system.

Это верхняя точка входа для:

- `arm + hand` direct `ros2_control`
- `arm + hand + MoveIt`
- `rover` direct bringup

Текущий пакет вырос из старого `silverhand_moveit2` и теперь играет роль общего orchestration-layer.

## Что включает

- arm model/control:
  - `silverhand_arm_model`
  - `silverhand_arm_control`
- hand model/control:
  - `silverhand_hand_model`
  - `silverhand_hand_control`
- rover direct launch:
  - `silverhand_rover_control`
- MoveIt config:
  - SRDF
  - OMPL
  - controller mapping
  - RViz config

## Зависимости

- Ubuntu 24.04
- ROS 2 Jazzy

Минимально:

```bash
sudo apt-get update
sudo apt-get install -y \
  ros-jazzy-moveit \
  ros-jazzy-joint-state-publisher \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-ros2-control \
  ros-jazzy-controller-manager \
  ros-jazzy-joint-trajectory-controller \
  ros-jazzy-joint-state-broadcaster \
  ros-jazzy-xacro
```

## Workspace layout

Ожидаемый layout:

```bash
~/silver_ws/src/silverhand_arm_model
~/silver_ws/src/silverhand_arm_control
~/silver_ws/src/silverhand_hand_model
~/silver_ws/src/silverhand_hand_control
~/silver_ws/src/silverhand_rover_control
~/silver_ws/src/silverhand_system_bringup
```

Опционально:

```bash
~/silver_ws/src/silverhand_system_description
```

## Сборка

```bash
cd ~/silver_ws
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
```

## Основные launch-файлы

### Arm + hand direct

```bash
ros2 launch silverhand_system_bringup silverhand_system_arm_hand_direct.launch.py use_mock_hardware:=true
```

Обёртки:

```bash
ros2 launch silverhand_system_bringup silverhand_system_arm_hand_direct_mock.launch.py
ros2 launch silverhand_system_bringup silverhand_system_arm_hand_direct_real.launch.py
```

### Arm + hand + MoveIt

```bash
ros2 launch silverhand_system_bringup silverhand_system_arm_hand_moveit.launch.py use_mock_hardware:=true use_rviz:=false
```

Это сейчас основной launch для robot-side `MoveIt` smoke/integration tests.

### Rover only

```bash
ros2 launch silverhand_system_bringup silverhand_system_rover.launch.py use_mock_hardware:=true
```

Обёртки:

```bash
ros2 launch silverhand_system_bringup silverhand_system_rover_mock.launch.py
ros2 launch silverhand_system_bringup silverhand_system_rover_real.launch.py
```

### Viewer only

```bash
ros2 launch silverhand_system_bringup silverhand_system_view.launch.py
```

## Helper scripts

В пакете есть стандартные helper-скрипты запуска.

Базовые shorthand-режимы:

```bash
cd /home/r/silver_ws/src/silverhand_system_bringup
./scripts/start_system_mock.sh
./scripts/start_system_real.sh
./scripts/start_system_gui.sh
./scripts/start_system_view.sh
```

Явные сценарии:

```bash
./scripts/start_system_arm_hand_direct_mock.sh
./scripts/start_system_arm_hand_direct_real.sh
./scripts/start_system_arm_hand_moveit_mock.sh
./scripts/start_system_arm_hand_moveit_real.sh
./scripts/start_system_rover_mock.sh
./scripts/start_system_rover_real.sh
```

Поддерживаемые переменные окружения:

- `ROS_WS`
- `ROS_DISTRO`
- `SILVERHAND_USE_RVIZ`
- `SILVERHAND_ARM_CAN_IFACE`
- `SILVERHAND_ARM_NODE_ID`
- `SILVERHAND_HAND_CAN_IFACE`
- `SILVERHAND_HAND_NODE_ID`
- `SILVERHAND_ROVER_CAN_IFACE`
- `SILVERHAND_ROVER_NODE_ID`
- `SILVERHAND_ROVER_QUEUE_LEN`

## Role-based launch

### Robot machine

```bash
ros2 launch silverhand_system_bringup silverhand_system_robot.launch.py use_mock_hardware:=true
```

### GUI machine

```bash
ros2 launch silverhand_system_bringup silverhand_system_gui.launch.py
```

Без RViz:

```bash
ros2 launch silverhand_system_bringup silverhand_system_gui.launch.py use_rviz:=false
```

## Что реально протестировано

На текущий момент подтвержден рабочий сценарий:

- `silverhand_system_arm_hand_moveit.launch.py`
- `use_mock_hardware:=true`
- `use_rviz:=false`
- robot-side `ws_gateway --mode moveit`
- GUI подключается по websocket и шлёт `set_joint_goal`

По этой схеме реально проходят:

- planning через `MoveGroup`
- execution через `arm_controller`
- `joint_state` обратно в GUI

## Полезные проверки

Контроллеры:

```bash
ros2 control list_controllers
```

Ожидаемо активны:

- `joint_state_broadcaster`
- `arm_controller`
- `hand_controller`

Action server MoveIt:

```bash
ros2 action list | grep move_action
```

Action server direct arm control:

```bash
ros2 action list | grep follow_joint_trajectory
```

## Логи

Если поднимаешь через `nohup`, удобно вести:

- `~/silver_ws/run_logs/system_bringup_moveit.log`

В этом логе обычно ищутся:

- `MoveGroupMoveAction: Received request`
- `Solution was found and executed`
- `START_STATE_INVALID`
- `GOAL_STATE_INVALID`
- сообщения от `arm_controller` / `hand_controller`

## systemd

Для `systemd --user` есть template:

- `systemd/user/silverhand-system-bringup@.service`

Поддерживаемые instance-имена:

- `mock`
- `real`
- `gui`
- `view`
- `arm_hand_direct_mock`
- `arm_hand_direct_real`
- `arm_hand_moveit_mock`
- `arm_hand_moveit_real`
- `rover_mock`
- `rover_real`

Установка:

```bash
mkdir -p ~/.config/systemd/user
cp /home/r/silver_ws/src/silverhand_system_bringup/systemd/user/silverhand-system-bringup@.service ~/.config/systemd/user/
systemctl --user daemon-reload
```

Примеры запуска:

```bash
systemctl --user enable --now silverhand-system-bringup@arm_hand_moveit_mock.service
systemctl --user enable --now silverhand-system-bringup@arm_hand_direct_real.service
systemctl --user enable --now silverhand-system-bringup@rover_mock.service
```

Автозапуск на старте системы без интерактивного логина:

```bash
loginctl enable-linger "$USER"
```

Полезные команды:

```bash
systemctl --user status silverhand-system-bringup@arm_hand_moveit_mock.service
journalctl --user -u silverhand-system-bringup@arm_hand_moveit_mock.service -f
systemctl --user restart silverhand-system-bringup@arm_hand_moveit_mock.service
systemctl --user disable --now silverhand-system-bringup@arm_hand_moveit_mock.service
```

## Важные замечания

- arm joints сейчас `continuous`, то есть жёстких position bounds у руки в URDF нет
- реальные жёсткие limits есть у пальцев
- не все ошибки `START_STATE_INVALID` означают “плохие joint limits”; часто это уже вопрос валидности стартового состояния в `MoveIt`
- `link_4 ↔ hand_gripper_link` сейчас не отключён в `SRDF`, потому что эта самоколлизия может быть полезной и должна отслеживаться честно

## Ближайшее развитие

- единый `full-system` bringup для rover + arm + hand
- дальнейшее согласование controller managers / robot descriptions
- интеграция `nav2`
- работа с единым system-level websocket gateway
