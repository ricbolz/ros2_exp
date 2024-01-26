import math
import time
import rclpy
from rclpy.node import Node
from raspimouse_msgs.msg import LightSensors, Switches

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
        self.switches_sub = self.create_subscription(Switches, 'switches', self.callback_switches, 1)

        # 現在のセンサの値
        self.sensor_values = [0, 0, 0, 0]
        self.can_publish_cmdvel = False

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

    def callback_switches(self, msg):
        self.switches = msg
        if self.line_sampling or self.field_sampling:
            return

        if self.switches.switch0:
            if self.sampling_is_done() and not self.can_publish_cmdvel:
                self.get_logger().info("Start following.")
                self.set_motor_power(True)
                self.beep_success()
                self.can_publish_cmdvel = True
            else:
                self.get_logger().info("Stop following.")
                self.set_motor_power(False)
                self.beep_failure()
                self.can_publish_cmdvel = False
        elif self.switches.switch1:
            self.get_logger().info("line sampling:")
            self.beep_start()
            self.line_sampling = True
        elif self.switches.switch2:
            self.get_logger().info("field sampling:")
            self.beep_start()
            self.field_sampling = True

def main():
    rclpy.init()

    node = LightsensorMonitor()

    rclpy.spin(node)

    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()