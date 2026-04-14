# silverhand_system_bringup

Верхнеуровневый bringup-пакет для оркестрации SilverHand.

Каноническая сущностная модель:

- `arm`
- `arm_hand`
- `rover`
- `system = rover + arm + hand`

Режимы:

- `arm`: `mock`, `ros_control`, `moveit`
- `arm_hand`: `mock`, `ros_control`, `moveit`
- `rover`: `mock`, `ros_control`
- `system`: `mock`, `ros_control`, `moveit`

`silverhand_system_bringup` оркестрирует запуск. Источник правды для hardware transport defaults лежит в нижних пакетах:

- [silverhand_arm_control/config/hardware_profiles.yaml](../silverhand_arm_control/config/hardware_profiles.yaml)
- [silverhand_hand_control/config/hardware_profiles.yaml](../silverhand_hand_control/config/hardware_profiles.yaml)
- [silverhand_rover_control/config/hardware_profiles.yaml](../silverhand_rover_control/config/hardware_profiles.yaml)

## Что делает пакет

- оркестрация MoveIt только для руки
- оркестрация MoveIt для руки и захвата
- оркестрация полной системы rover+arm+hand
- точки входа GUI
- просмотр только в RViz

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

## Структура workspace

Ожидаемый layout:

```bash
~/silver_ws/src/silverhand_arm_model
~/silver_ws/src/silverhand_arm_control
~/silver_ws/src/silverhand_hand_model
~/silver_ws/src/silverhand_hand_control
~/silver_ws/src/silverhand_rover_model
~/silver_ws/src/silverhand_rover_control
~/silver_ws/src/silverhand_system_bringup
```

Опционально:

```bash
~/silver_ws/src/silverhand_rover_teleop
~/silver_ws/src/silverhand_system_description
```

## Сборка

```bash
cd ~/silver_ws
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
```

## Канонические launch-файлы

### Arm

```bash
ros2 launch silverhand_system_bringup silverhand_system_arm_mock.launch.py
ros2 launch silverhand_system_bringup silverhand_system_arm_ros_control.launch.py
ros2 launch silverhand_system_bringup silverhand_system_arm_moveit.launch.py use_mock_hardware:=true use_rviz:=false
```

### Arm + Hand

```bash
ros2 launch silverhand_system_bringup silverhand_system_arm_hand_mock.launch.py
ros2 launch silverhand_system_bringup silverhand_system_arm_hand_ros_control.launch.py
ros2 launch silverhand_system_bringup silverhand_system_arm_hand_moveit.launch.py use_mock_hardware:=true use_rviz:=false
```

### Rover

```bash
ros2 launch silverhand_system_bringup silverhand_system_rover_mock.launch.py
ros2 launch silverhand_system_bringup silverhand_system_rover_ros_control.launch.py
```

Низкоуровневый passthrough:

```bash
ros2 launch silverhand_system_bringup silverhand_system_rover.launch.py
```

`silverhand_system_rover.launch.py` просто включает upstream [silverhand_rover_bringup.launch.py](../silverhand_rover_control/launch/silverhand_rover_bringup.launch.py). Значения по умолчанию для rover transport и IMU задаются в `silverhand_rover_control`.

### Full System

Mock:

```bash
ros2 launch silverhand_system_bringup silverhand_system_mock.launch.py
```

ros2_control:

```bash
ros2 launch silverhand_system_bringup silverhand_system_ros_control.launch.py
```

MoveIt:

```bash
ros2 launch silverhand_system_bringup silverhand_system_moveit.launch.py use_mock_hardware:=true use_rviz:=false
```

Full-system launch использует:

- rover как root `base_link`
- arm links с префиксом `arm_`
- arm joints без префикса `joint_1..joint_6`
- hand joints `hand_left_finger_joint` и `hand_right_finger_joint`

Это позволяет держать совместимость с существующими arm controllers и MoveIt-конфигом, но убрать конфликт `base_link` между rover и arm.

## GUI и визуализация

Arm GUI:

```bash
ros2 launch silverhand_system_bringup silverhand_system_gui_arm.launch.py
```

Rover GUI:

```bash
ros2 launch silverhand_system_bringup silverhand_system_gui_rover.launch.py
```

RViz-only viewer:

```bash
ros2 launch silverhand_system_bringup silverhand_system_view_only_rviz.launch.py
```

Ролевой arm+hand MoveIt без RViz:

```bash
ros2 launch silverhand_system_bringup silverhand_system_arm_hand_robot.launch.py use_mock_hardware:=true
```

## Вспомогательные скрипты

Канонические scripts:

```bash
./scripts/start_system_mock.sh
./scripts/start_system_ros_control.sh
./scripts/start_system_moveit.sh
./scripts/start_system_arm_mock.sh
./scripts/start_system_arm_ros_control.sh
./scripts/start_system_arm_moveit.sh
./scripts/start_system_arm_hand_mock.sh
./scripts/start_system_arm_hand_ros_control.sh
./scripts/start_system_arm_hand_moveit.sh
./scripts/start_system_rover_mock.sh
./scripts/start_system_rover_ros_control.sh
./scripts/start_system_gui_arm.sh
./scripts/start_system_gui_rover.sh
./scripts/start_system_view_only_rviz.sh
```

Скрипт для ролевого сценария:

```bash
./scripts/start_system_arm_hand_robot.sh
```

## Переменные окружения

Общие:

- `ROS_WS`
- `ROS_DISTRO`
- `SILVERHAND_USE_RVIZ`
- `SILVERHAND_USE_MOCK_HARDWARE`

Переопределения rover:

- `SILVERHAND_ROVER_CAN_IFACE`
- `SILVERHAND_ROVER_NODE_ID`
- `SILVERHAND_ROVER_QUEUE_LEN`
- `SILVERHAND_ROVER_USE_IMU_ODOMETRY`
- `SILVERHAND_ROVER_USE_POWER_BOARD`
- `SILVERHAND_ROVER_POWER_BOARD_CLIENT_NODE_ID`

Параметры rover GUI:

- `SILVERHAND_ROVER_GUI_HOST`
- `SILVERHAND_ROVER_GUI_PORT`

Важно:

- arm/hand transport defaults больше не задаются в `silverhand_system_bringup`
- system-level rover overrides здесь только переопределяют defaults из `silverhand_rover_control`, но не заменяют источник правды

## systemd

Шаблон systemd-сервиса:

- [silverhand-system-bringup@.service](systemd/system/silverhand-system-bringup@.service)

Установка:

```bash
sudo install -Dm644 systemd/system/silverhand-system-bringup@.service /etc/systemd/system/silverhand-system-bringup@.service
sudo systemctl daemon-reload
```

Канонические имена экземпляров:

```bash
sudo systemctl start silverhand-system-bringup@mock
sudo systemctl start silverhand-system-bringup@ros_control
sudo systemctl start silverhand-system-bringup@moveit
sudo systemctl start silverhand-system-bringup@arm_mock
sudo systemctl start silverhand-system-bringup@arm_ros_control
sudo systemctl start silverhand-system-bringup@arm_moveit
sudo systemctl start silverhand-system-bringup@arm_hand_mock
sudo systemctl start silverhand-system-bringup@arm_hand_ros_control
sudo systemctl start silverhand-system-bringup@arm_hand_moveit
sudo systemctl start silverhand-system-bringup@rover_mock
sudo systemctl start silverhand-system-bringup@rover_ros_control
sudo systemctl start silverhand-system-bringup@gui_arm
sudo systemctl start silverhand-system-bringup@gui_rover
sudo systemctl start silverhand-system-bringup@view_only_rviz
```

Ролевой экземпляр:

```bash
sudo systemctl start silverhand-system-bringup@arm_hand_robot
```

## Примечания к реализации

URDF полной системы:

- [silverhand_system.urdf.xacro](urdf/silverhand_system.urdf.xacro)

Ядро launch полной системы:

- [silverhand_system_full_common.launch.py](launch/silverhand_system_full_common.launch.py)

SRDF полной системы:

- [system.srdf](config/system.srdf)

## Проверено

Проверено:

- `python3 -m py_compile launch/*.launch.py`
- `bash -n scripts/*.sh`
- `colcon build --packages-select silverhand_arm_model silverhand_system_bringup`
- `xacro` для full-system URDF разворачивается с rover `base_link`, arm links `arm_*` и arm joints `joint_1..joint_6`
- `ros2 launch ... --show-args` для
  - `silverhand_system_mock.launch.py`
  - `silverhand_system_ros_control.launch.py`
  - `silverhand_system_moveit.launch.py`
