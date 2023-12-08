import random
import pygame
import Const

class Enemy(pygame.sprite.Sprite):
    elements = {
        "無" : 0,
        "木" : 1,
        "火" : 2,
        "土" : 3,
        "金" : 4,
        "水" : 5,
    }

    def __init__(self, level, road, x, y):
        super().__init__()
        self.level = level
        self.hp = 0
        self.max_hp = 0
        self.speed = 0
        self.element = 0
        self.grid = (x, y) # グリッドの座標
        self.pos = self.grid_to_absolute(x, y) # 絶対座標
        self.road = road # 道の情報
        self.vec = 0 # 進行方向 0:上, 1:右, 2:下, 3:左
        self.goal = 0 # ゴールの座標
        self.decide_direction() # 進行方向を決める
        self.distance = self.count_distance() # ゴールまでの距離
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect(center=self.pos)

    # グリッドの座標を絶対座標に変換する
    def grid_to_absolute(self, x, y):
        absolute_x = x * Const.CELL_WIDTH + (1280 - Const.YOKO) // 2
        absolute_y = y * Const.CELL_HEIGHT
        absolute_x += Const.CELL_WIDTH // 2
        absolute_y += Const.CELL_HEIGHT // 2
        return (absolute_x, absolute_y)

    # 絶対座標をグリッドの座標に変換する
    def absolute_to_grid(self, x, y):
        grid_x = int((x - (1280 - Const.YOKO) // 2) // Const.CELL_WIDTH)
        grid_y = int(y // Const.CELL_HEIGHT)
        return (grid_x, grid_y)

    def is_alive(self):
        return self.hp > 0

    # ゴールまでの距離を計算する
    def count_distance(self):
        return abs(self.pos[0] - self.road["goal"][0][0]) + abs(self.pos[1] - self.road["goal"][0][1])

    # コアに到達したかどうかを判定する
    def is_reached(self):
        return self.grid == self.road["goal"][0]

    # 座標をうけとって、表示する
    def display(self, screen):
        # hpバーを表示する
        hp_bar_width = 20
        hp_bar_height = 3
        hp_bar_x = self.pos[0] - hp_bar_width // 2
        hp_bar_y = self.pos[1] - Const.CELL_HEIGHT // 2 - hp_bar_height
        hp_bar = pygame.Rect(hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height)
        pygame.draw.rect(screen, (255, 0, 0), hp_bar)
        hp_bar_width = int(self.hp / self.max_hp * 20)
        hp_bar = pygame.Rect(hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height)
        pygame.draw.rect(screen, (0, 255, 0), hp_bar)
        
        # 敵を表示する
        screen.blit(self.image, self.rect)

    # 進むべき向きを決める
    def decide_direction(self):
        # 進むべき方向を決める
        # 進むべき方向がない場合は、その場にとどまる
        if self.road["road"][self.grid[1]][self.grid[0]] == []:
            return
        # 進むべき方向がある場合は、進むべき方向を決める
        if len(self.road["road"][self.grid[1]][self.grid[0]]) == 1:
            # 現在のグリッドと比較して、進むべき方向を決める
            next_grid = self.road["road"][self.grid[1]][self.grid[0]][0]
            if next_grid[0] == self.grid[0] and next_grid[1] == self.grid[1] - 1:
                self.goal = self.grid_to_absolute(self.grid[0], self.grid[1] - 1)
                self.vec = 0
            elif next_grid[0] == self.grid[0] + 1 and next_grid[1] == self.grid[1]:
                self.goal = self.grid_to_absolute(self.grid[0] + 1, self.grid[1])
                self.vec = 1
            elif next_grid[0] == self.grid[0] and next_grid[1] == self.grid[1] + 1:
                self.goal = self.grid_to_absolute(self.grid[0], self.grid[1] + 1)
                self.vec = 2
            elif next_grid[0] == self.grid[0] - 1 and next_grid[1] == self.grid[1]:
                self.goal = self.grid_to_absolute(self.grid[0] - 1, self.grid[1])
                self.vec = 3
        # 進むべき方向が複数ある場合は、ランダムに進むべき方向を決める
        else:
            next_grid = self.road["road"][self.grid[1]][self.grid[0]]
            next_grid = next_grid[random.randint(0, len(next_grid) - 1)]
            if next_grid[0] == self.grid[0] and next_grid[1] == self.grid[1] - 1:
                self.goal = self.grid_to_absolute(self.grid[0], self.grid[1] - 1)
                self.vec = 0
            elif next_grid[0] == self.grid[0] + 1 and next_grid[1] == self.grid[1]:
                self.goal = self.grid_to_absolute(self.grid[0] + 1, self.grid[1])
                self.vec = 1
            elif next_grid[0] == self.grid[0] and next_grid[1] == self.grid[1] + 1:
                self.goal = self.grid_to_absolute(self.grid[0], self.grid[1] + 1)
                self.vec = 2
            elif next_grid[0] == self.grid[0] - 1 and next_grid[1] == self.grid[1]:
                self.goal = self.grid_to_absolute(self.grid[0] - 1, self.grid[1])
                self.vec = 3

    # 移動する
    def move(self):
        # 進む距離を計算する
        distance = (self.speed / 3) / Const.FPS
        # 進むべき方向に進む
        if self.vec == 0:
            self.pos = (self.pos[0], self.pos[1] - distance)
        elif self.vec == 1:
            self.pos = (self.pos[0] + distance, self.pos[1])
        elif self.vec == 2:
            self.pos = (self.pos[0], self.pos[1] + distance)
        elif self.vec == 3:
            self.pos = (self.pos[0] - distance, self.pos[1])
        
        # グリッドの座標を更新する
        self.grid = self.absolute_to_grid(self.pos[0], self.pos[1])
        self.distance = self.count_distance()

        # 目的地に到達したら、目的地を更新する
        if (self.vec == 0 and self.pos[1] <= self.goal[1]) or \
           (self.vec == 1 and self.pos[0] >= self.goal[0]) or \
           (self.vec == 2 and self.pos[1] >= self.goal[1]) or \
           (self.vec == 3 and self.pos[0] <= self.goal[0]):
            self.decide_direction()

        # 画像の位置を更新する
        self.rect.center = self.pos


class Mouse(Enemy):
    def __init__(self, level, road, x, y):
        super().__init__(level, road, x, y)
        self.hp = 30
        self.max_hp = 30
        self.speed = 90
        self.element = 0
