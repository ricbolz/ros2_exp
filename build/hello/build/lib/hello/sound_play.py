import pygame
import rclpy
from rclpy.node import Node

class SoundPlayerNode() :
    def __init__(self):
        pygame.mixer.init()
        self.node = rclpy.create_node('sound_player')
        self.sub = self.node.create_subscription(
            String,
            'sound_play',
            self.callback,
            10
        )

        def init_pygame(self):
            pygame.mixer.init()
            