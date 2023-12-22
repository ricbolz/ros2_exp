from pynput.keyboard import Listener,Key, KeyCode
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

#
# キーボードの基本クラス
#
class Keyboard(Node):
    #
    # コンストラクタ
    #
    def __init__(self):
        super().__init__('keyboard_controller')
        
        self.key_publisher = self.create_publisher(
            String, 
            'key_command',
            1)

        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)

    # タイマーによって呼び出される関数
    def timer_callback(self):
        # 以下の命令でキー入力に反応するようになる
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    #
    # キーが押されたときに呼び出される関数
    #
    def on_press(self, key):
        msg = String()
        # if isinstance(key, KeyCode):
        #     # 押されたキーをメッセージ文字列として登録
        #     msg.data = key.char
        #     # パブリッシュ
        #     self.key_publisher.publish(msg)                
    
    #
    # キーが離されたときに呼び出される関数
    #
    def on_release(self, key):
        msg = String()
        
        if isinstance(key, KeyCode):
            # 押されたキーをメッセージ文字列として登録
            msg.data = key.char
        #
        # その他のシンボルについては以下のURLを参照
        # https://pythonhosted.org/pynput/keyboard.html#controlling-the-keyboard
        #
        elif key == key.up:
            msg.data = 'up'
        elif key == key.down:
            msg.data = 'down'
        elif key == key.left:
            msg.data = 'left'
        elif key == key.right:
            msg.data = 'right'
        elif key == key.enter:
            msg.data = 'enter'            
        # パブリッシュ
        self.key_publisher.publish(msg)

def main():
    rclpy.init()

    node = Keyboard()

    rclpy.spin(node)

    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()