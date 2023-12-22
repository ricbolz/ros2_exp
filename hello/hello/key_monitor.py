import rclpy
from rclpy.node import Node
from std_msgs.msg import String

#
# キーボードからの入力を受け取るクラス
#
class KeyMonitor(Node):
    #
    # コンストラクタ
    #
    def __init__(self):
        super().__init__('keyboard_monitor')

        # キーボード入力を受け取るサブスクライバ
        self.key_subscription = self.create_subscription(
            String,
            'key_command',
            self.callback_keyboard,
            1)

    #
    # キーボードの値の受け取り
    #
    def callback_keyboard(self, msg):
        print('Command {} is recieved.'.format(msg.data))

        
def main():
    rclpy.init()

    node = KeyMonitor()

    rclpy.spin(node)

    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
