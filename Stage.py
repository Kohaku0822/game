from collections import defaultdict
import pygame
import Screen
import Const
import Tower
import Enemy
import Core
import Map

class Stage:
    def __init__(self, map_info):
        pygame.init()
        self.screen = Screen.MainScreen().screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("ipaexg.ttf", 24)  # ipaexg.ttfを読み込んでフォントとする
        self.map_data = map_info.map_data
        self.road = map_info.road
        self.core = Core.Core()
        self.tower_list = defaultdict(Tower.Tower)
        self.enemy_list = []
        pygame.display.set_caption(self.map_data["name"])
        
    def run(self):
        running = True
        while running:
            self.clock.tick(Const.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # マウスボタンを押したとき
                    if event.button == 1:
                        mouse_grid_x, mouse_grid_y = self.get_mouse_grid() 
                        if 0 <= mouse_grid_x < Const.GRID_WIDTH and 0 <= mouse_grid_y < Const.GRID_HEIGHT:
                            if self.map_data["map"][mouse_grid_y][mouse_grid_x] == 1:
                                self.set_tower(mouse_grid_x, mouse_grid_y) # タワーを設置する
                        # 一旦、敵を出現させる
                        if 0 <= mouse_grid_x < Const.GRID_WIDTH and 0 <= mouse_grid_y < Const.GRID_HEIGHT:
                            if self.map_data["map"][mouse_grid_y][mouse_grid_x] == 4:
                                self.spawn(mouse_grid_x, mouse_grid_y) # 敵を出現させる
                    elif event.button == 3:  # 右クリックのとき
                        mouse_grid_x, mouse_grid_y = self.get_mouse_grid() 
                        if 0 <= mouse_grid_x < Const.GRID_WIDTH and 0 <= mouse_grid_y < Const.GRID_HEIGHT:
                            if self.map_data["map"][mouse_grid_y][mouse_grid_x] == 2:
                                self.map_data["map"][mouse_grid_y][mouse_grid_x] = 1  # タワーを削除する
                                del self.tower_list[(mouse_grid_x, mouse_grid_y)]
            
            # 描画する
            self.display()
    
    # タワーを設置する
    def set_tower(self, x, y):
        # 制作中
        # とりあえず、一萬を設置する
        self.map_data["map"][y][x] = 2
        tower = Tower.M_1(x, y)
        self.tower_list[(x, y)] = tower
    
    # 敵を出現させる
    def spawn(self, x, y):
        # 制作中
        # とりあえず、ねずみを出現させる
        enemy = Enemy.Mouse(1, self.road, x, y)
        self.enemy_list.append(enemy)

    # マウスの位置を取得してグリッドを返す
    def get_mouse_grid(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        grid_x = (1280 - Const.YOKO) // 2
        grid_y = 0
        mouse_grid_x = (mouse_x - grid_x) // Const.CELL_WIDTH
        mouse_grid_y = (mouse_y - grid_y) // Const.CELL_HEIGHT
        return (mouse_grid_x, mouse_grid_y)

    # 画面を表示する
    def display(self):    
        # 画面のクリア
        self.screen.fill((255, 255, 255))  # 白色に変更

        # グリッドを表示
        grid_x = (1280 - Const.YOKO) // 2
        grid_y = 0
        pygame.draw.rect(self.screen, (0, 0, 0), (grid_x, grid_y, Const.YOKO, Const.TATE), 1)  # 外枠の色を黒色に変更
        for x in range(0, Const.YOKO, Const.CELL_WIDTH):
            pygame.draw.line(self.screen, (0, 0, 0), (grid_x + x, grid_y), (grid_x + x, grid_y + Const.TATE))  # グリッドの縦線の色を黒色に変更
        for y in range(0, Const.TATE, Const.CELL_HEIGHT):
            pygame.draw.line(self.screen, (0, 0, 0), (grid_x, grid_y + y), (grid_x + Const.YOKO, grid_y + y))  # グリッドの横線の色を黒色に変更
        
        # 色を定義
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        GRAY = (128, 128, 128)
        BROWN = (165, 42, 42)
        LIGHT_GYAY = (211, 211, 211)

        # マップを表示
        mp = self.map_data["map"]
        for y in range(Const.GRID_HEIGHT):
            for x in range(Const.GRID_WIDTH):
                if mp[y][x] == 0:
                    pygame.draw.rect(self.screen, BLACK, (grid_x + x * Const.CELL_WIDTH, grid_y + y * Const.CELL_HEIGHT, Const.CELL_WIDTH, Const.CELL_HEIGHT))
                elif mp[y][x] == 1:
                    pygame.draw.rect(self.screen, GRAY, (grid_x + x * Const.CELL_WIDTH, grid_y + y * Const.CELL_HEIGHT, Const.CELL_WIDTH, Const.CELL_HEIGHT))
                elif mp[y][x] == 2:
                    pygame.draw.rect(self.screen, RED, (grid_x + x * Const.CELL_WIDTH, grid_y + y * Const.CELL_HEIGHT, Const.CELL_WIDTH, Const.CELL_HEIGHT))
                elif mp[y][x] == 3:
                    pygame.draw.rect(self.screen, BROWN, (grid_x + x * Const.CELL_WIDTH, grid_y + y * Const.CELL_HEIGHT, Const.CELL_WIDTH, Const.CELL_HEIGHT))
                elif mp[y][x] == 4:
                    pygame.draw.rect(self.screen, BROWN, (grid_x + x * Const.CELL_WIDTH, grid_y + y * Const.CELL_HEIGHT, Const.CELL_WIDTH, Const.CELL_HEIGHT))
                elif mp[y][x] == 5:
                    pygame.draw.rect(self.screen, BROWN, (grid_x + x * Const.CELL_WIDTH, grid_y + y * Const.CELL_HEIGHT, Const.CELL_WIDTH, Const.CELL_HEIGHT))
                elif mp[y][x] == 6:
                    pygame.draw.rect(self.screen, BROWN, (grid_x + x * Const.CELL_WIDTH, grid_y + y * Const.CELL_HEIGHT, Const.CELL_WIDTH, Const.CELL_HEIGHT))
                elif mp[y][x] == 7:
                    pygame.draw.rect(self.screen, BROWN, (grid_x + x * Const.CELL_WIDTH, grid_y + y * Const.CELL_HEIGHT, Const.CELL_WIDTH, Const.CELL_HEIGHT))
                elif mp[y][x] == 8:
                    pygame.draw.rect(self.screen, BLUE, (grid_x + x * Const.CELL_WIDTH, grid_y + y * Const.CELL_HEIGHT, Const.CELL_WIDTH, Const.CELL_HEIGHT))
                elif mp[y][x] == 9:
                    pygame.draw.rect(self.screen, BLUE, (grid_x + x * Const.CELL_WIDTH, grid_y + y * Const.CELL_HEIGHT, Const.CELL_WIDTH, Const.CELL_HEIGHT))

        # マウスの位置を取得し、少し薄い色で描画
        mouse_grid_x, mouse_grid_y = self.get_mouse_grid() 
        if 0 <= mouse_grid_x < Const.GRID_WIDTH and 0 <= mouse_grid_y < Const.GRID_HEIGHT:
            pygame.draw.rect(self.screen, LIGHT_GYAY, (grid_x + mouse_grid_x * Const.CELL_WIDTH, grid_y + mouse_grid_y * Const.CELL_HEIGHT, Const.CELL_WIDTH, Const.CELL_HEIGHT), 1)
        # タワーにカーソルを合わせたとき、タワーの範囲を表示する
        if (mouse_grid_x, mouse_grid_y) in self.tower_list:
            tower = self.tower_list[(mouse_grid_x, mouse_grid_y)]
            pygame.draw.circle(self.screen, WHITE, tower.pos, tower.atk_range*Const.ATK_RANGE, 1)
        
        # 攻撃処理
        for tower in self.tower_list.values():
            tower.attack(self.enemy_list, pygame.time.get_ticks() / 1000, self.screen)

        # 敵を移動させる
        for enemy in self.enemy_list:
            enemy.move()
            if not enemy.is_alive():
                self.enemy_list.remove(enemy)
        
        # 敵がコアに到達したかどうかを判定する
        for enemy in self.enemy_list:
            if enemy.is_reached():
                self.core.damage(1)
                self.enemy_list.remove(enemy)
            if not self.core.is_alive():
                print("ゲームオーバー")
                running = False


        # 敵を表示
        for enemy in self.enemy_list:
            enemy.display(self.screen)

        # 画面の更新
        pygame.display.flip()