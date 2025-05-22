import pygame

# Config
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
PLAYER_SIZE = BLOCK_SIZE
GRAVITY = 1
JUMP_FORCE = -14.5
SPEED = 7

# Colors
BACKGROUND = (30, 30, 30)
SPIKE_COLOR = (180, 0, 0)
GROUND_COLOR = (100, 100, 100)
GOAL_COLOR = (0, 255, 0)

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, BLOCK_SIZE))
        self.image.fill(GROUND_COLOR)
        self.rect = self.image.get_rect(topleft=(0, HEIGHT - BLOCK_SIZE))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original = pygame.image.load("assets/skin.png").convert_alpha()
        original = pygame.transform.scale(original, (PLAYER_SIZE, PLAYER_SIZE))
        self.original_image = original
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation_speed = -8
        self.reset()

    def reset(self):
        self.rect.topleft = (50, HEIGHT - BLOCK_SIZE - PLAYER_SIZE)
        self.velocity_y = 0
        self.on_ground = True
        self.angle = 0
        self.rotated_image = self.original_image.copy()

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False

    def update(self, platforms, spikes, ground, goals):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        if not self.on_ground:
            self.angle += self.rotation_speed
            self.rotated_image = pygame.transform.rotozoom(self.original_image, self.angle % 360, 1)
        else:
            self.rotated_image = self.original_image

        self.on_ground = False
        if self.rect.colliderect(ground.rect) and self.velocity_y >= 0:
            self.rect.bottom = ground.rect.top
            self.velocity_y = 0
            self.on_ground = True

        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True

        for spike in spikes:
            offset_x = spike.rect.left - self.rect.left
            offset_y = spike.rect.top - self.rect.top
            if self.mask.overlap(spike.mask, (offset_x, offset_y)):
                return "dead"
        for goal in goals:
            offset_x = goal.rect.left - self.rect.left
            offset_y = goal.rect.top - self.rect.top
            if self.mask.overlap(goal.mask, (offset_x, offset_y)):
                return "win"
        return None

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill((120, 120, 120))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x -= SPEED

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, direction="up"):
        super().__init__()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        self.direction = direction

        if direction == "up":
            points = [(0, BLOCK_SIZE), (BLOCK_SIZE // 2, 0), (BLOCK_SIZE, BLOCK_SIZE)]
        elif direction == "down":
            points = [(0, 0), (BLOCK_SIZE // 2, BLOCK_SIZE), (BLOCK_SIZE, 0)]
        elif direction == "left":
            points = [(BLOCK_SIZE, 0), (0, BLOCK_SIZE // 2), (BLOCK_SIZE, BLOCK_SIZE)]
        else:
            points = [(0, 0), (BLOCK_SIZE, BLOCK_SIZE // 2), (0, BLOCK_SIZE)]

        pygame.draw.polygon(self.image, SPIKE_COLOR, points)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= SPEED

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(GOAL_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= SPEED

LEVEL = [
    {'type': 'block', 'x': 0, 'y': HEIGHT - BLOCK_SIZE, 'width': 10},
    {'type': 'spike', 'x': 220, 'y': HEIGHT - 2 * BLOCK_SIZE, 'direction': 'up'},
    {'type': 'spike', 'x': 240, 'y': HEIGHT - 2 * BLOCK_SIZE, 'direction': 'up'},
    {'type': 'spike', 'x': 260, 'y': HEIGHT - 2 * BLOCK_SIZE, 'direction': 'up'},
    {'type': 'block', 'x': 320, 'y': HEIGHT - 3 * BLOCK_SIZE, 'width': 3},
    {'type': 'block', 'x': 400, 'y': HEIGHT - 2 * BLOCK_SIZE, 'width': 5},
    {'type': 'spike', 'x': 520, 'y': HEIGHT - 2 * BLOCK_SIZE, 'direction': 'up'},
    {'type': 'block', 'x': 550, 'y': HEIGHT - 4 * BLOCK_SIZE, 'width': 3},
    {'type': 'block', 'x': 625, 'y': HEIGHT - BLOCK_SIZE, 'width': 5},
    {'type': 'goal', 'x': 675, 'y': HEIGHT - 2 * BLOCK_SIZE},
]

def generate_level():
    blocks = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    goals = pygame.sprite.Group()
    for element in LEVEL:
        if element['type'] == 'block':
            for i in range(element.get('width', 1)):
                block = Block(element['x'] + i * BLOCK_SIZE, element['y'])
                blocks.add(block)
        elif element['type'] == 'spike':
            spike = Spike(element['x'], element['y'], element.get('direction', 'up'))
            spikes.add(spike)
        elif element['type'] == 'goal':
            goal = Goal(element['x'], element['y'])
            goals.add(goal)
    return blocks, spikes, goals