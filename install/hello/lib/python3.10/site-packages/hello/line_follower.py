import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int16
from geometry_msgs.msg import Twist
from lifecycle_msgs.srv import ChangeState
from raspimouse_msgs.msg import LightSensors, Switches, Leds
from std_srvs.srv import SetBool
from rclpy.executors import MultiThreadedExecutor
import time

class LineFollower(Node):
    NUM_OF_SAMPLES = 10
    SENSOR_NUM = 4

    def __init__(self):
        # super().__init__('follower', namespace='', node_options=options)
        super().__init__('follower')
        self.switches = Switches()
        self.present_sensor_values = [0] * self.SENSOR_NUM
        self.sensor_line_values = [0] * self.SENSOR_NUM
        self.sensor_field_values = [0] * self.SENSOR_NUM
        self.line_thresholds = [0] * self.SENSOR_NUM
        self.sampling_values = [0] * self.SENSOR_NUM
        self.line_is_detected_by_sensor = [False] * self.SENSOR_NUM
        self.sampling_count = 0
        self.line_values_are_sampled = False
        self.field_values_are_sampled = False
        self.line_sampling = False
        self.field_sampling = False
        self.can_publish_cmdvel = False

        self.cmd_vel_timer = self.create_timer(0.05, self.on_cmd_vel_timer)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 1)
        self.buzzer_pub = self.create_publisher(Int16, 'buzzer', 1)
        self.leds_pub = self.create_publisher(Leds, 'leds', 1)
        self.light_sensors_sub = self.create_subscription(LightSensors, 'light_sensors', self.callback_light_sensors, 1)
        self.switches_sub = self.create_subscription(Switches, 'switches', self.callback_switches, 1)
        self.motor_power_client = self.create_client(SetBool, 'motor_power')

    def on_cmd_vel_timer(self):
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
        
        self.switches = Switches()  # Reset switch values

        if self.can_publish_cmdvel:
            self.publish_cmdvel_for_line_following()

        self.indicate_line_detections()

    def callback_light_sensors(self, msg):
        # The order of the front distance sensors and the line following sensors are not the same
        self.present_sensor_values[0] = msg.forward_r
        self.present_sensor_values[1] = msg.right
        self.present_sensor_values[2] = msg.left
        self.present_sensor_values[3] = msg.forward_l

        if self.line_sampling or self.field_sampling:
            self.multisampling()

        if self.sampling_is_done():
            self.update_line_detection()

    def callback_switches(self, msg):
        self.switches = msg

    def set_motor_power(self, motor_on):
        request = SetBool.Request()
        request.data = motor_on
        future_result = self.motor_power_client.call_async(request)

    def publish_cmdvel_for_line_following(self):
        VEL_LINEAR_X = 0.08  # m/s
        VEL_ANGULAR_Z = 0.8  # rad/s
        LOW_VEL_ANGULAR_Z = 0.5  # rad/s

        cmd_vel = Twist()

        detect_line = any(self.line_is_detected_by_sensor)
        detect_field = any(not x for x in self.line_is_detected_by_sensor)

        if detect_line and detect_field:
            cmd_vel.linear.x = VEL_LINEAR_X

            if self.line_is_detected_by_sensor[0]:
                cmd_vel.angular.z += VEL_ANGULAR_Z
            if self.line_is_detected_by_sensor[3]:
                cmd_vel.angular.z -= VEL_ANGULAR_Z
            if self.line_is_detected_by_sensor[1]:
                cmd_vel.angular.z += LOW_VEL_ANGULAR_Z
            if self.line_is_detected_by_sensor[2]:
                cmd_vel.angular.z -= LOW_VEL_ANGULAR_Z

        self.cmd_vel_pub.publish(cmd_vel)

    def update_line_detection(self):
        for i in range(self.SENSOR_NUM):
            is_positive = self.present_sensor_values[i] > self.line_thresholds[i]
            self.line_is_detected_by_sensor[i] = is_positive == self.line_is_bright()

    def line_is_bright(self):
        SAMPLE = 3
        return self.sensor_line_values[SAMPLE] > self.sensor_field_values[SAMPLE]

    def indicate_line_detections(self):
        msg = Leds()
        msg.led0 = self.line_is_detected_by_sensor[3]
        msg.led1 = self.line_is_detected_by_sensor[1]
        msg.led2 = self.line_is_detected_by_sensor[2]
        msg.led3 = self.line_is_detected_by_sensor[0]
        self.leds_pub.publish(msg)

    def beep_buzzer(self, freq, beep_time):
        msg = Int16()
        msg.data = freq
        self.buzzer_pub.publish(msg)

        time.sleep(beep_time)

        msg = Int16()
        msg.data = 0
        self.buzzer_pub.publish(msg)

    def beep_start(self):
        self.beep_buzzer(1000, 0.5)

    def beep_success(self):
        self.beep_buzzer(1000, 0.1)
        time.sleep(0.1)
        self.beep_buzzer(1000, 0.1)

    def beep_failure(self):
        for _ in range(4):
            self.beep_buzzer(500, 0.1)
            time.sleep(0.1)

    def sampling_is_done(self):
        return self.line_values_are_sampled and self.field_values_are_sampled

    def multisampling(self):
        if self.sampling_count < self.NUM_OF_SAMPLES:
            for i in range(self.SENSOR_NUM):
                self.sampling_values[i] += self.present_sensor_values[i]
            self.sampling_count += 1
        else:
            for i in range(self.SENSOR_NUM):
                self.sampling_values[i] /= self.NUM_OF_SAMPLES

            if self.line_sampling:
                self.sensor_line_values = self.sampling_values.copy()
                self.line_values_are_sampled = True
            else:
                self.sensor_field_values = self.sampling_values.copy()
                self.field_values_are_sampled = True

            self.sampling_count = 0
            self.sampling_values = [0] * self.SENSOR_NUM
            self.line_sampling = self.field_sampling = False

            self.get_logger().info(
                f"L:{self.sensor_line_values[0]}, ML:{self.sensor_line_values[1]}, "
                f"MR:{self.sensor_line_values[2]}, R:{self.sensor_line_values[3]}"
            )

            self.set_line_thresholds()
            self.beep_success()

    def median(self, value1, value2):
        diff = abs(value1 - value2)
        if value1 < value2:
            return value1 + diff * 0.5
        else:
            return value2 + diff * 0.5

    def set_line_thresholds(self):
        if not self.sampling_is_done():
            return

        for i in range(self.SENSOR_NUM):
            self.line_thresholds[i] = self.median(
                self.sensor_line_values[i], self.sensor_field_values[i]
            )

        self.get_logger().info(
            f"line_thresholds: L:{self.line_thresholds[0]}, ML:{self.line_thresholds[1]}, "
            f"MR:{self.line_thresholds[2]}, R:{self.line_thresholds[3]}"
        )

def main():
    rclpy.init()
    node = LineFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
