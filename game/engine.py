# game/engine.py
from .entities import Player, Platform, Obstacle
from .level import LEVEL_DATA
from config import OBSTACLE_SPEED, WIDTH, HEIGHT, FPS
class GameEngine:
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.platforms = []
        self.level_index = 0
        self.world_x = 0
        self.score = 0
        self.game_over = False
        self.id = False 

    def reset(self):
        self.__init__()

    def spawn_objects(self, screen_width):
        while (self.level_index < len(LEVEL_DATA) and 
               LEVEL_DATA[self.level_index]["x"] <= self.world_x + screen_width):
            data = LEVEL_DATA[self.level_index]
            spawn_x = screen_width + (data["x"] - self.world_x)
            obj_id = data.get("id")
            if self.id:
                if data["type"] == "obstacle":
                    self.obstacles.append(Obstacle(spawn_x, OBSTACLE_SPEED, obj_id=obj_id))
                elif data["type"] == "obstacle_air":
                    self.obstacles.append(Obstacle(spawn_x, OBSTACLE_SPEED, y=data["y"], obj_id=obj_id))
                elif data["type"] == "platform":
                    self.platforms.append(Platform(spawn_x, data["y"], data["width"], OBSTACLE_SPEED, obj_id=obj_id))
                self.level_index += 1
            elif self.id==False:
                if data["type"] == "obstacle":
                    self.obstacles.append(Obstacle(spawn_x, OBSTACLE_SPEED))
                elif data["type"] == "obstacle_air":
                    self.obstacles.append(Obstacle(spawn_x, OBSTACLE_SPEED, y=data["y"]))
                elif data["type"] == "platform":
                    self.platforms.append(Platform(spawn_x, data["y"], data["width"], OBSTACLE_SPEED))
                self.level_index += 1


    def update(self, jump_pressed, screen_width):
        if self.game_over:
            return

        self.world_x += OBSTACLE_SPEED
        self.spawn_objects(screen_width)

        self.player.update(self.platforms, self.obstacles)
        for o in self.obstacles: o.update()
        for p in self.platforms: p.update()

        self.obstacles = [o for o in self.obstacles if not o.off_screen()]
        self.platforms = [p for p in self.platforms if not p.off_screen()]

        if jump_pressed:
            self.player.jump()

        if not self.player.alive:
            self.game_over = True

        self.score += 1

    def is_done(self):
        return self.game_over or self.world_x > 9500

    def get_reward(self):
        if not self.player.alive:
            return -100
        if self.world_x > 9500:
            return 1000
        return 0.1