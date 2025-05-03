# dofbot\_vision

## Dofbot Simulation & Color Vision Demo

This project demonstrates a simulated Dofbot robot in RViz, integrated with a basic OpenCV-based color recognition system for detecting colored blocks. The full ROS 2 pipeline includes:

* A URDF-based Dofbot model rendered in RViz
* A static image publisher node
* A color vision processing node using OpenCV
* Visualization of detection results (bounding boxes + RViz markers)

---

## Prerequisites

* Docker
* WSL2 or native Linux (Ubuntu 22.04 recommended)
* X11 display server (e.g., WSLg or native Linux X server)
* (Optional) NVIDIA GPU for Gazebo or real camera integration

---

## 1. Build & Run the Docker Container

From the project root:

```bash
# Build the Docker image
docker build -t ros_sim:humble -f docker/Dockerfile .

# Run the container, mount the workspace
docker run -it --rm \
  --network host \
  -e DISPLAY=$DISPLAY \
  -v /mnt/wslg/.X11-unix:/tmp/.X11-unix \
  -v ~/dofbot_vision/ros_ws:/ros_ws \
  ros_sim:humble
```

---

## 2. Build the ROS 2 Workspace

Inside the container:

```bash
cd /ros_ws
colcon build --symlink-install
source install/setup.bash
```

This builds:

* `dofbot_description` (URDF + RViz config)
* `color_vision` (static image publisher + vision node)

---

## 3. Visualize the Dofbot in RViz

```bash
ros2 launch dofbot_description display.launch.py
```

This starts:

* `joint_state_publisher_gui` – interactive joint sliders
* `robot_state_publisher` – publishes TF from URDF
* `rviz2` – with the `dofbot_humble.rviz` configuration loaded

---

## 4. Run the Color Vision Demo

### A. Static Image Publisher

Publishes a test JPEG to `/camera/image_raw`:

```bash
ros2 run color_vision static_image_publisher \
  --ros-args -p image_path:=/ros_ws/src/color_vision/images/colored_blocks_1.jpg
```

### B. Color Vision Node

Subscribes to `/camera/image_raw`, detects color regions, and publishes:

* Annotated image → `/camera/segmented`
* Markers → `/detection_markers`

```bash
ros2 run color_vision color_vision
```

### C. Static TF Publisher

Publishes a static transform between `map` and `camera_frame`:

```bash
ros2 run tf2_ros static_transform_publisher \
  --x 0 --y 0 --z 0 \
  --roll 0 --pitch 0 --yaw 0 \
  --frame-id map --child-frame-id camera_frame
```

---

## 5. Visualize Results in RViz

Open RViz with the color vision layout:

```bash
rviz2 -d /ros_ws/src/color_vision/rviz/new_config.rviz
```

You should see:

* Live image (`/camera/segmented`)
* Detected regions as green boxes
* Markers at detection sites
* TF tree rooted at `map` with child `camera_frame`

---

## Notes

* you can tweak the HSV ranges in `color_vision.py` to refine detection accuracy
* for real-time use replace the static image publisher with a camera driver node
