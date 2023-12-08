# タイトル画面を表示するクラス
import pygame
import Screen
import StageSelect

class TitleScreen:
    def __init__(self):
        pygame.init()
        self.screen = Screen.MainScreen().screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("ipaexg.ttf", 24)  # ipaexg.ttfを読み込んでフォントとする
        pygame.display.set_caption("Title")
        self.start_button = pygame.Rect(300, 200, 200, 50)
        self.quit_button = pygame.Rect(300, 300, 200, 50)
        self.options_button = pygame.Rect(300, 400, 200, 50)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.start_button.collidepoint(event.pos):
                            stage_select = StageSelect.StageSelect()
                            stage_select.display()
                        elif self.quit_button.collidepoint(event.pos):
                            running = False
                        elif self.options_button.collidepoint(event.pos):
                            print("オプションボタンがクリックされました")

            self.screen.fill((255, 255, 255))
            
            # ボタンを描画する
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()
            button_width = self.start_button.width
            button_height = self.start_button.height
            button_x = (screen_width - button_width) // 2
            button_y = (screen_height - button_height) // 2 + 100
            self.start_button.topleft = (button_x, button_y)
            self.quit_button.topleft = (button_x, button_y + button_height + 10)
            self.options_button.topleft = (button_x, button_y + 2 * (button_height + 10))
            
            pygame.draw.rect(self.screen, (0, 0, 0), self.start_button)
            pygame.draw.rect(self.screen, (0, 0, 0), self.quit_button)
            pygame.draw.rect(self.screen, (0, 0, 0), self.options_button)
            start_text = self.font.render("はじめる", True, (255, 255, 255))
            quit_text = self.font.render("おわる", True, (255, 255, 255))
            options_text = self.font.render("オプション", True, (255, 255, 255))
            self.screen.blit(start_text, (self.start_button.x + 50, self.start_button.y + 10))
            self.screen.blit(quit_text, (self.quit_button.x + 60, self.quit_button.y + 10))
            self.screen.blit(options_text, (self.options_button.x + 30, self.options_button.y + 10))
            pygame.display.flip()
            self.clock.tick(60)

# 単体テスト
if __name__ == "__main__":
    title_screen = TitleScreen()
    title_screen.run()