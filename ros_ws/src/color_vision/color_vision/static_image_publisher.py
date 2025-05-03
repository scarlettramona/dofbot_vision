#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2, os

class StaticImagePublisher(Node):
    def __init__(self):
        super().__init__('static_image_publisher')
        # parameter for image path
        self.declare_parameter('image_path', '/ros_ws/src/color_vision/test.jpg')
        path = self.get_parameter('image_path').get_parameter_value().string_value
        if not os.path.isfile(path):
            self.get_logger().error(f"Image not found: {path}")
            rclpy.shutdown()
            return
        self.img = cv2.imread(path)
        self.bridge = CvBridge()
        self.pub = self.create_publisher(Image, 'camera/image_raw', 10)
        self.create_timer(1.0, self.timer_cb)  # 1 Hz

    def timer_cb(self):
        msg = self.bridge.cv2_to_imgmsg(self.img, 'bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg = self.bridge.cv2_to_imgmsg(self.img, 'bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_frame'
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = StaticImagePublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
