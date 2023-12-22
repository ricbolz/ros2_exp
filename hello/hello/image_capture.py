import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

#
# カメラから映像を取得して送信するクラス
#
class ImageCapture(Node):
    #
    # コンストラクタ
    #
    def __init__(self):
        super().__init__('imaga_capture')

        # 画像データのパブリッシャ
        self.image_publisher = self.create_publisher(
            Image,
            'cap_image',
            1)

        timer_period = 0.03
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.cv_bridge = CvBridge()
        self.capture = cv2.VideoCapture(0)
        #
        # 使用可能な解像度とフレームレートは,
        # v4l2-ctl --list-formats-ext
        # で調べることができる.
        #
        self.capture.set(cv2.CAP_PROP_FPS, 30)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)        

    # タイマーで呼び出される関数
    def timer_callback(self):
        ret, image = self.capture.read()
        self.image_publisher.publish(self.cv_bridge.cv2_to_imgmsg(image, "bgr8"))

def main():
    rclpy.init()

    node = ImageCapture()

    rclpy.spin(node)

    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()