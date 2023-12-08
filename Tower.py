import pygame
import Const
import Enemy

# 親クラス
class Tower:
    elements = {
        "無" : 0,
        "木" : 1,
        "火" : 2,
        "土" : 3,
        "金" : 4,
        "水" : 5,
    }

    def __init__(self, x, y):
        self.level = 1
        self.atk = 0
        self.atk_range = 0
        self.atk_speed = 0
        self.atk_cnt = 1   # 1:単体, 2~:範囲
        self.type = 0       # 0:萬子, 1:筒子, 2:索子, 3:字牌
        self.num = 0        # 数牌の場合の数字
        self.element = 0    # 0:無, 1:木, 2:火, 3:土, 4:金, 5:水
        self.grid = (x, y) # グリッドの座標
        self.pos = self.grid_to_absolute(x, y) # 絶対座標
        self.last_attack_time = 0
        self.cost = 0
        self.upgrade_cost = 0


    def upgrade(self):
        self.level += 1
        self.atk += 0
        self.atk_range += 0
        self.atk_speed += 0
        self.upgrade_cost += 0
    
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

    def attack(self, enemy_list, current_time, screen):
        # 現在の時間が最後の攻撃時間から一定の間隔を超えていなければ、攻撃しない
        if current_time - self.last_attack_time < 2.0 / self.atk_speed:
            return

        # コアに近い敵を優先して攻撃する
        enemy_list.sort(key=lambda enemy: enemy.distance)
        cnt = self.atk_cnt
        for enemy in enemy_list:
            # タワーの攻撃範囲内に敵がいるかどうかを判定する
            if self.is_in_range(enemy):
                print("敵に攻撃した", enemy.pos, self.pos, cnt)
                enemy.hp -= self.atk
                # 最後の攻撃時間を更新する
                self.last_attack_time = current_time
                cnt -= 1
                if cnt == 0:
                    break
                
        
        
    
    def is_in_range(self, enemy):
        # 敵とタワーの距離を計算する
        distance = self.calc_distance(enemy)
        # 敵とタワーの距離がタワーの攻撃範囲内かどうかを判定する
        return distance <= self.atk_range * Const.ATK_RANGE

    def calc_distance(self, enemy):
        # 敵とタワーの座標を取得する
        enemy_x, enemy_y = enemy.pos
        tower_x, tower_y = self.pos
        # 座標間の距離を計算する
        distance = ((enemy_x - tower_x) ** 2 + (enemy_y - tower_y) ** 2) ** 0.5
        return distance
        

# 牌の種類クラス
class Manzu(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 0
        self.atk_cnt = 1

class Pinzu(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 1
        self.atk_cnt = 999

class Souzu(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 2
        self.atk_cnt = 1

class Jihai(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 3
        self.atk_cnt = 1

# 萬子クラス
class M_1(Manzu):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.atk = 10
        self.atk_range = 3
        self.atk_speed = 2
        self.element = self.elements["水"]
        self.cost = 1
        self.upgrade_cost = 1
        self.num = 1

class M_2(Manzu):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.atk = 6
        self.atk_range = 3
        self.atk_speed = 4
        self.cost = 1
        self.upgrade_cost = 1
        self.num = 2

class M_3(Manzu):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.atk = 10
        self.atk_range = 3
        self.atk_speed = 2
        self.element = self.elements["木"]
        self.cost = 1
        self.upgrade_cost = 1
        self.num = 3

class M_4(Manzu):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.atk = 6
        self.atk_range = 5
        self.atk_speed = 2
        self.cost = 1
        self.upgrade_cost = 1
        self.num = 4

class M_5(Manzu):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.atk = 10
        self.atk_range = 3
        self.atk_speed = 2
        self.element = self.elements["土"]
        self.cost = 1
        self.upgrade_cost = 1
        self.num = 5

class M_6(Manzu):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.atk = 4
        self.atk_range = 5
        self.atk_speed = 4
        self.cost = 1
        self.upgrade_cost = 1
        self.num = 6

class M_7(Manzu):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.atk = 10
        self.atk_range = 3
        self.atk_speed = 2
        self.element = self.elements["金"]
        self.cost = 1
        self.upgrade_cost = 1
        self.num = 7

class M_8(Manzu):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.atk = 24
        self.atk_range = 3
        self.atk_speed = 1
        self.cost = 1
        self.upgrade_cost = 1
        self.num = 8

class M_9(Manzu):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.atk = 10
        self.atk_range = 3
        self.atk_speed = 2
        self.element = self.elements["火"]
        self.cost = 1
        self.upgrade_cost = 1
        self.num = 9
