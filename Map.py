# mapdata/mapxx.pyを読み込んでインスタンスを生成するためのクラス
import Const

class Map:
    def __init__(self, map_num):
        self.map_num = map_num
        self.map_data = self.load_map_data()
        self.road = self.load_road()
    
    def load_map_data(self):
        try:
            # map_numに対応するmapxx.pyを読み込んでインスタンスを生成する
            map_data = __import__("mapdata.map{:02d}".format(self.map_num), fromlist=["mapdata"])
            return map_data.map_data
        except:
            print("mapdata/map{:02d}.pyが見つかりませんでした。".format(self.map_num))
            return None
    
    def load_road(self):
        road = {
            "start" : [],
            "goal" : [],
            "road" : [[[] for _ in range(Const.GRID_WIDTH)] for i in range(Const.GRID_HEIGHT)],
        }

        # map_data["map"]を読み込んで、startを探す
        for y, row in enumerate(self.map_data["map"]):
            for x, cell in enumerate(row):
                if cell == 4:
                    road["start"].append((x, y))
        
        # map_data["map"]を読み込んで、goalを探す
        for y, row in enumerate(self.map_data["map"]):
            for x, cell in enumerate(row):
                if cell == 8:
                    road["goal"].append((x, y))
        
        # startを起点に深さ優先探索で道を探す
        for road_start in road["start"]:
            self.dfs(road_start, road)
        return road
    
    def dfs(self, pos, road):
        x = pos[0]
        y = pos[1]
        if road["road"][y][x] != []:
            return
        
        # 上下左右の道を探す
        if y > 0 and self.map_data["map"][y - 1][x] == 3:
            if road["road"][y - 1][x] == []:
                road["road"][y][x].append((x, y - 1))
                self.dfs((x, y - 1), road)
        if y < Const.GRID_HEIGHT - 1 and self.map_data["map"][y + 1][x] == 3:
            if road["road"][y + 1][x] == []:
                road["road"][y][x].append((x, y + 1))
                self.dfs((x, y + 1), road)
        if x > 0 and self.map_data["map"][y][x - 1] == 3:
            if road["road"][y][x - 1] == []:
                road["road"][y][x].append((x - 1, y))
                self.dfs((x - 1, y), road)
        if x < Const.GRID_WIDTH - 1 and self.map_data["map"][y][x + 1] == 3:
            if road["road"][y][x + 1] == []:
                road["road"][y][x].append((x + 1, y))
                self.dfs((x + 1, y), road)