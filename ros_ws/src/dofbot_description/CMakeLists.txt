# ros_ws/src/dofbot_description/CMakeLists.txt

cmake_minimum_required(VERSION 3.5)
project(dofbot_description)

find_package(ament_cmake REQUIRED)

# install the entire urdf/ folder into share/dofbot_description/urdf
install(
  DIRECTORY urdf meshes rviz launch config
  DESTINATION share/${PROJECT_NAME}
)

install(
  FILES package.xml
  DESTINATION share/${PROJECT_NAME}
)
ament_package()
