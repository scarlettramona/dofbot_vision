# docker/ros2_sim/Dockerfile

FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble


RUN apt-get update && apt-get install -y wget gnupg2 lsb-release \
 && wget -qO - https://packages.osrfoundation.org/gazebo.key | apt-key add - \
 && echo "deb [arch=$(dpkg --print-architecture)] \
        http://packages.osrfoundation.org/gazebo/ubuntu-stable \
        $(lsb_release -cs) main" \
    > /etc/apt/sources.list.d/gazebo-stable.list


RUN apt-get update && apt-get install -y \
      gazebo \
      ros-humble-ros-ign \
      ros-humble-gazebo-ros-pkgs \
      ros-humble-ros-ign-gazebo \
      ros-humble-ros-ign-bridge \
      ros-humble-ros2-control \
      ros-humble-ros2-controllers \
      ros-humble-controller-manager \
      ros-humble-joint-state-publisher-gui \
      ros-humble-xacro \
      ros-humble-moveit \
      ros-humble-ament-cmake \
      libopencv-dev python3-opencv \
      ros-humble-cv-bridge \
      ros-humble-visualization-msgs \
      curl git python3-pip python3-colcon-common-extensions \
      libopencv-dev python3-opencv \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /ros_ws

RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash"      >> /root/.bashrc && \
    echo "source /ros_ws/install/setup.bash"           >> /root/.bashrc && \
    printf "source /opt/ros/$ROS_DISTRO/setup.bash\n"   >  /etc/profile.d/ros2_workspace.sh && \
    printf "source /ros_ws/install/setup.bash\n"      >> /etc/profile.d/ros2_workspace.sh && \
    chmod +x /etc/profile.d/ros2_workspace.sh

ENTRYPOINT ["/bin/bash"]
CMD ["-i"]
