class Core:
    def __init__(self):
        self.hp = 5
    
    def is_alive(self):
        return self.hp > 0

    def damage(self, damage):
        self.hp -= damage