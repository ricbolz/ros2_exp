import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from raspimouse_msgs.msg import LightSensors, Switches, Leds
from std_srvs.srv import SetBool
from std_msgs.msg import String, Int16

class robot_node(Node):

    NUM_OF_SAMPLES = 10
    SENSOR_NUM = 4

    def __init__(self):
        super().__init__('robot_node')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.listener_callback,
            10)
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            'cmd_vel',
            10)
        # self.switch_sub = self.create_subscription(
        #     Switches,
        #     'switches',
        #     self.switch_callback,
        #     10)
        self.buzzer_pub = self.create_publisher(
            Int16,
            'buzzer',
        10)
        self.switches = Switches()
        self.cmd_vel_timer = self.create_timer(0.05, self.on_cmd_vel_timer)
        self.light_sensors_sub = self.create_subscription(LightSensors, 'light_sensors', self.callback_light_sensors, 1)
        self.switches_sub = self.create_subscription(Switches, 'switches', self.switch_callback, 1)
        self.motor_power_client = self.create_client(SetBool, 'motor_power')

        self.publisher = self.create_publisher(String, 'hello_topic', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0

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
        
        
        self.velocity = 0.0

    def timer_callback(self) :
        msg =String()
        msg.data = 'Hello World(%d)' % self.count
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"'% msg.data)
        self.count+=1

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

        #self.indicate_line_detections()

    def listener_callback(self, msg):
        twist = Twist()

        # For a PS2 controller, the left stick's x-axis (usually msg.axes[0]) controls the direction
        twist.angular.z = msg.axes[0] 
        

        # Check if the 'X' button (usually msg.buttons[2] for a PS2 controller) is pressed
        if msg.buttons[2] == 1:
            self.velocity += 0.01  # Increase the velocity
            if self.velocity > 0.2 :
                self.velocity = 0.2
            self.get_logger().info('The "X" button is pressed. Increasing velocity.')

        # Check if the 'Square' button (usually msg.buttons[3] for a PS2 controller) is pressed
        elif msg.buttons[3] == 1:
            self.velocity -= 0.01  # Decrease the velocity (act as brake)
            if self.velocity < -0.2 :
                self.velocity = -0.2
            self.get_logger().info('The "Square" button is pressed. Decreasing velocity.')
        else :
            self.velocity = 0.0
        # Apply the velocity
        twist.linear.x = self.velocity

        self.publisher.publish(twist)
        self.get_logger().info('Publishing Twist: linear.x=%f, angular.z=%f' % (twist.linear.x, twist.angular.z))

    def switch_callback(self, msg):
        self.switches = msg
        self.get_logger().info("Start following.")

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
    
    def update_line_detection(self):
        for i in range(self.SENSOR_NUM):
            is_positive = self.present_sensor_values[i] > self.line_thresholds[i]
            self.line_is_detected_by_sensor[i] = is_positive == self.line_is_bright()

    # def indicate_line_detections(self):
    #     msg = Leds()
    #     msg.led0 = self.line_is_detected_by_sensor[3]
    #     msg.led1 = self.line_is_detected_by_sensor[1]
    #     msg.led2 = self.line_is_detected_by_sensor[2]
    #     msg.led3 = self.line_is_detected_by_sensor[0]
    #     self.leds_pub.publish(msg)
        
    def beep_buzzer(self, freq, beep_time):
        msg = Int16()
        msg.data = freq
        self.buzzer_pub.publish(msg)

        time.sleep(beep_time)

        msg = Int16()
        msg.data = 0
        self.buzzer_pub.publish(msg)
    
    def set_motor_power(self, motor_on):
        request = SetBool.Request()
        request.data = motor_on
        future_result = self.motor_power_client.call_async(request)

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

    def publish_cmdvel_for_line_following(self):
        # VEL_LINEAR_X = 0.08  # m/s
        # VEL_ANGULAR_Z = 0.8  # rad/s
        # LOW_VEL_ANGULAR_Z = 0.5  # rad/s

        

        detect_line = any(self.line_is_detected_by_sensor)
        detect_field = any(not x for x in self.line_is_detected_by_sensor)

        if not detect_line or not detect_field:
            # cmd_vel.linear.x = VEL_LINEAR_X
            self.beep_failure()
            # if self.line_is_detected_by_sensor[0]:
            #     cmd_vel.angular.z += VEL_ANGULAR_Z
            # if self.line_is_detected_by_sensor[3]:
            #     cmd_vel.angular.z -= VEL_ANGULAR_Z
            # if self.line_is_detected_by_sensor[1]:
            #     cmd_vel.angular.z += LOW_VEL_ANGULAR_Z
            # if self.line_is_detected_by_sensor[2]:
            #     cmd_vel.angular.z -= LOW_VEL_ANGULAR_Z
            
        #self.cmd_vel_pub.publish(cmd_vel)
            
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
    node = robot_node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ =="__main__":
    main()