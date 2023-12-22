import math
import time
import rclpy
from rclpy.node import Node
from raspimouse_msgs.msg import LightSensors

#
# ライトセンサの値を取得するクラス
#
class LightsensorMonitor(Node):
    #
    # コンストラクタ
    #
    def __init__(self):
        super().__init__('lightsernsor_monitor')

        # ライトセンサーの値を受け取るサブスクライバ
        self.lightsensor_subscription = self.create_subscription(
            LightSensors,
            'light_sensors',
            self.callback_lightsensors,
            1
        )

        # 現在のセンサの値
        self.sensor_values = [0, 0, 0, 0]

    #
    # ライトセンサの値の受け取り
    #
    def callback_lightsensors(self, msg):   
        self.sensor_values[0] = msg.forward_r
        self.sensor_values[1] = msg.right
        self.sensor_values[2] = msg.left
        self.sensor_values[3] = msg.forward_l
        print('{}, {}, {}, {}'.format(self.sensor_values[0],
                                      self.sensor_values[1],
                                      self.sensor_values[2],
                                      self.sensor_values[3]))

def main():
    rclpy.init()

    node = LightsensorMonitor()

    rclpy.spin(node)

    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()