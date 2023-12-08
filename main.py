# このファイルを実行するとゲームが開始される
import pygame
import Title

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.font = pygame.font.Font("ipaexg.ttf", 24)  # ipaexg.ttfを読み込んでフォントとする

    def run(self):
        # タイトル画面を表示する
        title_screen = Title.TitleScreen()
        title_screen.run()

        # ゲームの終了処理
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()