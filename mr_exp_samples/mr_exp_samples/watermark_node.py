import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import cv_bridge

##
# https://shuzo-kino.hateblo.jp/entry/2023/10/11/215754
#

class WatermarkNode(Node):

    def __init__(self):
        super().__init__('watermark_node')
        self.subscriber = self.create_subscription(
            Image, 
            '/image_raw', self.image_callback, 10)
        self.publisher = self.create_publisher(Image, '/output_image_with_watermark', 10)
        self.bridge = cv_bridge.CvBridge()

    def image_callback(self, img_msg):
        # OpenCV の様式に変更
        cv_image = self.bridge.imgmsg_to_cv2(img_msg, desired_encoding='bgr8')

        # 透かしをいれる
        watermark = "Watermark Text Here"
        cv2.putText(cv_image, watermark, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # ROSの様式に戻す
        output_img_msg = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')

        # トピックとして配信する
        self.publisher.publish(output_img_msg)

def main(args=None):
    rclpy.init(args=args)
    watermark_node = WatermarkNode()
    rclpy.spin(watermark_node)
    watermark_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()