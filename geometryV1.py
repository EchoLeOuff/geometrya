import pygame
import sys

# Initialisation
pygame.init()

# Configuration
WIDTH, HEIGHT = 1200, 800
BLOCK_SIZE = 40
PLAYER_SIZE = BLOCK_SIZE
GRAVITY = 1
JUMP_FORCE = -14.5
SPEED = 7

# Couleurs
BACKGROUND = (30, 30, 30)
RED = (255, 0, 0)
SPIKE_COLOR = (180, 0, 0)
GROUND_COLOR = (100, 100, 100)

# Fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spikes Comportement Complexe")

SKIN_PLAYER = pygame.image.load("skin.png").convert_alpha()
SKIN_PLAYER = pygame.transform.scale(SKIN_PLAYER, (PLAYER_SIZE, PLAYER_SIZE))


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, BLOCK_SIZE))
        self.image.fill(GROUND_COLOR)
        self.rect = self.image.get_rect(topleft=(0, HEIGHT - BLOCK_SIZE))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = SKIN_PLAYER
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.rotation_speed = -8
        self.rotated_image = self.original_image
        self.reset()

    def reset(self):
        self.rect.topleft = (100, HEIGHT - BLOCK_SIZE - PLAYER_SIZE)
        self.velocity_y = 0
        self.on_ground = True
        self.angle = 0
        self.rotated_image = self.original_image.copy()

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False

    def update(self, platforms, spikes, ground):
        # ——— 1) PHYSIQUE VERTICALE ———
        # Applique la gravité et déplace verticalement
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        self.on_ground = False

        # Collision sol (même logique que pour une plateforme)
        if self.rect.colliderect(ground.rect) and self.velocity_y >= 0:
            self.rect.bottom = ground.rect.top
            self.velocity_y = 0
            self.on_ground = True

        # Collision plateformes : d’abord la verticale
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    # atterrissage
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    # coup de tête sous la plateforme
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

        # ——— 2) VISUEL (rotation) ———
        if not self.on_ground:
            self.angle = (self.angle + self.rotation_speed) % 360
            self.rotated_image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        else:
            self.rotated_image = self.original_image
        # Mettre à jour le masque pour la collision pixel-perfect
        self.mask = pygame.mask.from_surface(self.rotated_image)

        # ——— 3) RÉSOLUTION HORIZONTALE ———
        # (utile si un bloc se déplace dans le joueur)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # si le centre du joueur est à gauche de la plateforme, collision à droite
                if self.rect.centerx < platform.rect.centerx:
                    self.rect.right = platform.rect.left
                    return True
                else:
                    self.rect.left = platform.rect.right

        # ——— 4) COLLISION AVEC LES PICS ———
        for spike in spikes:
            # on recalcule l'offset en tenant compte du nouveau masque
            offset_x = spike.rect.left - self.rect.left
            offset_y = spike.rect.top - self.rect.top
            if self.mask.overlap(spike.mask, (offset_x, offset_y)):
                return True

        return False


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
        self.color = SPIKE_COLOR

        points = []
        if direction == "up":
            points = [(0, BLOCK_SIZE), (BLOCK_SIZE // 2, 0), (BLOCK_SIZE, BLOCK_SIZE)]
        elif direction == "down":
            points = [(0, 0), (BLOCK_SIZE // 2, BLOCK_SIZE), (BLOCK_SIZE, 0)]
        elif direction == "left":
            points = [(BLOCK_SIZE, 0), (0, BLOCK_SIZE // 2), (BLOCK_SIZE, BLOCK_SIZE)]
        else:
            points = [(0, 0), (BLOCK_SIZE, BLOCK_SIZE // 2), (0, BLOCK_SIZE)]

        pygame.draw.polygon(self.image, self.color, points)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= SPEED


LEVEL = [
    {'type': 'block', 'x': 0, 'y': HEIGHT - BLOCK_SIZE, 'width': 5},
    {'type': 'spike', 'x': 400, 'y': HEIGHT - 2 * BLOCK_SIZE, 'direction': 'up'},
    {'type': 'spike', 'x': 440, 'y': HEIGHT - 2 * BLOCK_SIZE, 'direction': 'up'},
    {'type' : 'block', 'x': 500, 'y': HEIGHT - 2 * BLOCK_SIZE, 'width': 5},
     {'type': 'block', 'x': 580, 'y': HEIGHT - 3 * BLOCK_SIZE, 'width': 5},

]


def generate_level():
    blocks = pygame.sprite.Group()
    spikes = pygame.sprite.Group()

    for element in LEVEL:
        if element['type'] == 'block':
            for i in range(element.get('width', 1)):
                block = Block(element['x'] + i * BLOCK_SIZE, element['y'])
                blocks.add(block)
        elif element['type'] == 'spike':
            spike = Spike(element['x'], element['y'], element.get('direction', 'up'))
            spikes.add(spike)

    return blocks, spikes


# Initialisation
ground = Ground()
player = Player()
all_blocks, all_spikes = generate_level()
deaths = 0
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

while True:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.jump()

    # Mise à jour
    all_blocks.update()
    all_spikes.update()
    dead = player.update(all_blocks, all_spikes, ground)

    if dead:
        deaths += 1
        player.reset()
        all_blocks, all_spikes = generate_level()

    # Affichage
    screen.blit(ground.image, ground.rect)
    all_blocks.draw(screen)
    all_spikes.draw(screen)

    screen.blit(player.rotated_image, player.rotated_image.get_rect(center=player.rect.center))

    # UI
    screen.blit(font.render(f"Morts: {deaths}", True, (255, 255, 255)), (20, 20))

    pygame.display.flip()
    clock.tick(60)