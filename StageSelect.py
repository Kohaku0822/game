# ステージ選択画面を表示するクラス
import pygame
import Screen
import Const
import Stage
import Map

class StageSelect:
    def __init__(self):
        pygame.init()
        self.stages = list(range(1, Const.STAGE_NUM + 1))
        self.current_page = 0
        self.items_per_row = 4
        self.items_per_page = 4 * self.items_per_row
        self.font = pygame.font.Font("ipaexg.ttf", 24)  # ipaexg.ttfを読み込んでフォントとする
        pygame.display.set_caption("Stage Select")
        self.screen = Screen.MainScreen().screen
        self.clock = pygame.time.Clock()

    def display(self):
        start_index = self.current_page * self.items_per_row
        end_index = start_index + self.items_per_page
        current_stages = self.stages[start_index:end_index]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        self.scroll("up")
                    elif event.button == 5:  # Scroll down
                        self.scroll("down")
                    elif event.button == 1:  # Left mouse button
                        if self.is_in_return_button(event.pos):
                            return
                        else:
                            for i, stage_item in enumerate(current_stages):
                                x = (i % self.items_per_row) * 150 + (self.screen.get_width() - self.items_per_row * 150) / 2
                                y = (i // self.items_per_row) * 100 + (self.screen.get_height() - (len(current_stages) // self.items_per_row) * 100) / 2
                                stage_rect = pygame.Rect(x, y, 130, 60)
                                if stage_rect.collidepoint(event.pos):
                                    print("ステージ{}がクリックされました".format(stage_item))
                                    # まだマップ2までしかないので、一旦それ以降は無視する
                                    if stage_item > 2:
                                        continue
                                    map_info = Map.Map(stage_item)
                                    stage = Stage.Stage(map_info)
                                    stage.run()
                
                # current_stagesを更新する
                start_index = self.current_page * self.items_per_row
                end_index = start_index + self.items_per_page
                current_stages = self.stages[start_index:end_index]

            self.screen.fill((255, 255, 255))

            for i, stage in enumerate(current_stages):
                x = (i % self.items_per_row) * 150 + (self.screen.get_width() - self.items_per_row * 150) / 2
                y = (i // self.items_per_row) * 100 + (self.screen.get_height() - (len(current_stages) // self.items_per_row) * 100) / 2
                text = self.font.render(str(stage), True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = (x + 65, y + 30)
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 130, 60), 2)
                self.screen.blit(text, text_rect)

            # 左上に戻るボタンを描画する
            return_button_rect = pygame.Rect(20, 20, 100, 40)
            pygame.draw.rect(self.screen, (0, 0, 0), return_button_rect, 2)
            return_button_text = self.font.render("戻る", True, (0, 0, 0))
            return_button_text_rect = return_button_text.get_rect()
            return_button_text_rect.center = return_button_rect.center
            self.screen.blit(return_button_text, return_button_text_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def scroll(self, direction):
        if direction == "up":
            self.current_page -= 1
        elif direction == "down":
            self.current_page += 1

        if self.current_page < 0:
            self.current_page = 0
        elif self.current_page >= len(self.stages) // self.items_per_row - 3:
            self.current_page = len(self.stages) // self.items_per_row - 4

    def is_in_return_button(self, pos):
        return_button_rect = pygame.Rect(20, 20, 100, 40)
        return return_button_rect.collidepoint(pos)


# 単体テスト
if __name__ == "__main__":
    stage_select = StageSelect()
    stage_select.display()