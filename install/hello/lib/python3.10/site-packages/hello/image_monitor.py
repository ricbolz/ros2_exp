import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

#
# 画像データを受け取って表示するクラス
#
class ImageMonitor(Node):
    #
    # コンストラクタ
    #
    def __init__(self):
        super().__init__('image_monitor')

        # 画像データのサブスクライバ
        self.image_subscription = self.create_subscription(
            Image,
            'cap_image',
            self.image_callback,
            1)

        self.cv_bridge = CvBridge()

    #
    # 画像データを受け取ったら呼び出される関数
    #
    def image_callback(self, image):
        cv_image = self.cv_bridge.imgmsg_to_cv2(image, "bgr8")
        if cv_image is not None:
            cv2.imshow("received image", cv_image)
            cv2.waitKey(1)
            
def main():
    rclpy.init()

    node = ImageMonitor()

    rclpy.spin(node)

    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()