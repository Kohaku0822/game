# 画面構成を管理するクラス
import pygame
import Const

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

class MainScreen(Screen):
    def __init__(self):
        super().__init__(Const.WINDOW_WIDTH , Const.WINDOW_HEIGHT)