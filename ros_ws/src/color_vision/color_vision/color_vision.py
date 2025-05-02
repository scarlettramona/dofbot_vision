#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from visualization_msgs.msg import Marker, MarkerArray
from cv_bridge import CvBridge
import cv2

class ColorVision(Node):
    def __init__(self):
        super().__init__('color_vision')
        self.bridge = CvBridge()
        self.pub_img = self.create_publisher(Image, 'camera/segmented', 10)
        self.pub_markers = self.create_publisher(MarkerArray, 'detection_markers', 10)
        self.create_subscription(Image, 'camera/image_raw', self.cb_image, 10)

    def cb_image(self, msg):
        # convert to OpenCV and HSV
        cv_img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        hsv   = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)

        ranges = {
          'red':   ((  0,100,100), ( 10,255,255)),
          'green': (( 40, 50, 50), ( 80,255,255)),
          'blue':  ((100, 50, 50), (130,255,255)),
        }

        markers   = MarkerArray()
        marker_id = 0

        for name, (lo, hi) in ranges.items():
            mask = cv2.inRange(hsv, lo, hi)

            # denoise
            mask = cv2.GaussianBlur(mask, (5,5), 0)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in cnts:
                area = cv2.contourArea(cnt)
                if area < 1000:             # filter small blobs
                    continue
                hull = cv2.convexHull(cnt)
                x,y,w,h = cv2.boundingRect(hull)
                cv2.rectangle(cv_img, (x,y),(x+w,y+h),(0,255,0),2)

                m = Marker()
                m.header.frame_id = msg.header.frame_id
                m.header.stamp    = msg.header.stamp
                m.ns        = 'blobs'
                m.id        = marker_id
                m.type      = Marker.CUBE
                m.action    = Marker.ADD
                m.pose.orientation.w = 1.0
                m.scale.x = m.scale.y = m.scale.z = 0.05
                m.color.g = 1.0; m.color.a = 0.8

                markers.markers.append(m)
                marker_id += 1

        out = self.bridge.cv2_to_imgmsg(cv_img, 'bgr8')
        out.header.stamp    = msg.header.stamp
        out.header.frame_id = msg.header.frame_id
        self.pub_img.publish(out)

        self.pub_markers.publish(markers)


def main(args=None):
    rclpy.init(args=args)
    node = ColorVision()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__=='__main__':
    main()
