import pygame
import sys

# --- Configuration ---
WIDTH, HEIGHT = 900, 500
FPS = 60
GRAVITY = 0.8
JUMP_VEL = -15
PLAYER_SIZE = 40
GROUND_HEIGHT = 80
OBSTACLE_SPEED = 7

SHOW_IDS = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash - Niveau Fixe Long")
clock = pygame.time.Clock()

# --- Couleurs ---
BG = (25, 25, 35)
GROUND_COLOR = (40, 40, 55)
PLAYER_COLOR = (255, 120, 120)
OBSTACLE_COLOR = (250, 210, 80)
PLATFORM_COLOR = (100, 180, 255)
TEXT_COLOR = (230, 230, 230)
font = pygame.font.Font(None, 24)

# --- Données de niveau (fixes) avec IDs ---
LEVEL_DATA = [
    # Départ: quelques petits obstacles bas
    {"id": 1,  "type": "obstacle",     "x": 600},
    {"id": 2,  "type": "obstacle",     "x": 900},
    {"id": 3,  "type": "obstacle",     "x": 1200},

    # Première plateforme pour apprendre à sauter dessus
    {"id": 4,  "type": "platform",     "x": 1500, "y": 320, "width": 180},

    # Séquence de sauts au sol
    {"id": 6,  "type": "obstacle",     "x": 1950},
    {"id": 7,  "type": "obstacle",     "x": 2200},
    {"id": 8,  "type": "obstacle",     "x": 2450},

    # Deux plateformes en escalier
    {"id": 9,  "type": "platform",     "x": 2700, "y": 340, "width": 160},
    {"id": 10, "type": "obstacle", "x": 2860},
    {"id": 11, "type": "obstacle", "x": 2910},
    {"id": 12, "type": "obstacle", "x": 2960},
    {"id": 13, "type": "obstacle", "x": 3010},
    {"id": 14, "type": "obstacle", "x": 3060},
    {"id": 15, "type": "obstacle", "x": 3110},
    {"id": 16, "type": "platform",     "x": 3125, "y": 330, "width": 200},

    # Corridor de plateformes
    {"id": 17, "type": "platform",     "x": 3550, "y": 320, "width": 160},
    {"id": 18, "type": "obstacle", "x": 3710},
    {"id": 19, "type": "obstacle", "x": 3760},

    {"id": 20, "type": "platform",     "x": 3800, "y": 310, "width": 140},
    {"id": 21, "type": "obstacle", "x": 3940},
    {"id": 22, "type": "obstacle", "x": 3990},
    {"id": 23, "type": "platform",     "x": 4050, "y": 280, "width": 140},

    # Obstacles plus rapprochés
    {"id": 24, "type": "obstacle",     "x": 4350},
    {"id": 25, "type": "obstacle",     "x": 4390},

    # Grande plateforme "safe"
    {"id": 26, "type": "platform",     "x": 5050, "y": 320, "width": 300},

    # --- Rallonge du parcours ---

    # Double pic au sol
    {"id": 27, "type": "obstacle",     "x": 5450},
    {"id": 28, "type": "obstacle",     "x": 5520},

    # Petite plateforme basse puis pic
    {"id": 29, "type": "platform",     "x": 5750, "y": 340, "width": 180},
    {"id": 30, "type": "obstacle",     "x": 6020},

    # Combo: plateforme moyenne + double pic
    {"id": 31, "type": "platform",     "x": 6150, "y": 310, "width": 200},
    {"id": 32, "type": "obstacle",     "x": 6550},
    {"id": 33, "type": "obstacle",     "x": 6620},

    # Passage de précision: triple pic espacé
    {"id": 34, "type": "obstacle",     "x": 6900},
    {"id": 35, "type": "obstacle",     "x": 6950},
    {"id": 36, "type": "obstacle",     "x": 7000},

    # Plateforme haute, oblige à bien timer les sauts
    {"id": 37, "type": "platform",     "x": 7400, "y": 365, "width": 220},
    {"id": 38, "type": "obstacle",     "x": 7700},

    # Double pic juste après une plateforme
    {"id": 39, "type": "platform",     "x": 7950, "y": 320, "width": 180},
    {"id": 40, "type": "obstacle",     "x": 8220},
    {"id": 41, "type": "obstacle",     "x": 8290},

    # Final: petite série de pics + grande plateforme de fin
    {"id": 42, "type": "obstacle",     "x": 8600},
    {"id": 43, "type": "obstacle",     "x": 8645},
    {"id": 44, "type": "platform",     "x": 9100, "y": 320, "width": 380},
]


# --- Classes principales ---
class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT - GROUND_HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
        self.vel_y = 0
        self.on_ground = False
        self.alive = True

    def jump(self):
        if self.on_ground and self.alive:
            self.vel_y = JUMP_VEL
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def handle_collisions(self, platforms, obstacles):
        self.on_ground = False

        # plateformes
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0 and self.rect.bottom <= p.rect.top + 10:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                else:
                    self.alive = False
                    return

        # obstacles (sol + air)
        for o in obstacles:
            if self.rect.colliderect(o.rect):
                self.alive = False
                return

        # sol
        if self.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.vel_y = 0
            self.on_ground = True

    def update(self, platforms, obstacles):
        if not self.alive:
            return
        self.apply_gravity()
        self.handle_collisions(platforms, obstacles)

    def draw(self, surf):
        color = PLAYER_COLOR if self.alive else (150, 50, 50)
        pygame.draw.rect(surf, color, self.rect)


class Platform:
    def __init__(self, x, y, width, speed, obj_id=None):
        self.rect = pygame.Rect(x, y, width, 20)
        self.speed = speed
        self.id = obj_id

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surf):
        pygame.draw.rect(surf, PLATFORM_COLOR, self.rect)
        if SHOW_IDS and self.id is not None:
            txt = font.render(str(self.id), True, TEXT_COLOR)
            text_rect = txt.get_rect(center=(self.rect.centerx, self.rect.top - 10))
            surf.blit(txt, text_rect)

    def off_screen(self):
        return self.rect.right < 0


class Obstacle:
    def __init__(self, x, speed, y=None, obj_id=None):
        # si y est None => pic au sol, sinon pic "en l'air" à hauteur y
        if y is None:
            base_y = HEIGHT - GROUND_HEIGHT - PLAYER_SIZE
        else:
            base_y = y - PLAYER_SIZE

        self.rect = pygame.Rect(
            x,
            base_y,
            PLAYER_SIZE,
            PLAYER_SIZE
        )
        self.speed = speed
        self.id = obj_id

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surf):
        left = self.rect.left
        right = self.rect.right
        bottom = self.rect.bottom
        top = self.rect.top

        points = [
            (left, bottom),
            (right, bottom),
            ((left + right) // 2, top)
        ]
        pygame.draw.polygon(surf, OBSTACLE_COLOR, points)

        if SHOW_IDS and self.id is not None:
            txt = font.render(str(self.id), True, TEXT_COLOR)
            text_rect = txt.get_rect(center=(self.rect.centerx, self.rect.top - 10))
            surf.blit(txt, text_rect)

    def off_screen(self):
        return self.rect.right < 0


# --- Fonction principale ---
def main():
    run = True
    player = Player()
    obstacles = []
    platforms = []
    score = 0
    game_over = False
    win = False  # indicateur de victoire

    level_index = 0
    world_x = 0

    while run:
        dt = clock.tick(FPS)
        screen.fill(BG)

        # événements (quitter + restart)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP) and (game_over or win):
                    player = Player()
                    obstacles.clear()
                    platforms.clear()
                    score = 0
                    game_over = False
                    win = False
                    level_index = 0
                    world_x = 0

        # touches maintenues pour saut continu
        keys = pygame.key.get_pressed()
        if not game_over and not win:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                player.jump()

        if not game_over and not win:
            world_x += OBSTACLE_SPEED

            # spawn des éléments du niveau
            while level_index < len(LEVEL_DATA) and LEVEL_DATA[level_index]["x"] <= world_x + WIDTH:
                data = LEVEL_DATA[level_index]
                spawn_x = WIDTH + (data["x"] - world_x)
                obj_id = data.get("id")

                if data["type"] == "obstacle":
                    obstacles.append(
                        Obstacle(spawn_x, OBSTACLE_SPEED, obj_id=obj_id)
                    )
                elif data["type"] == "obstacle_air":
                    obstacles.append(
                        Obstacle(spawn_x, OBSTACLE_SPEED, y=data["y"], obj_id=obj_id)
                    )
                elif data["type"] == "platform":
                    platforms.append(
                        Platform(spawn_x, data["y"], data["width"], OBSTACLE_SPEED, obj_id=obj_id)
                    )
                level_index += 1

            # update entités
            player.update(platforms, obstacles)
            for o in obstacles:
                o.update()
            for p in platforms:
                p.update()

            # nettoyage
            obstacles = [o for o in obstacles if not o.off_screen()]
            platforms = [p for p in platforms if not p.off_screen()]

            if not player.alive:
                game_over = True

            # mise à jour du score et test de victoire
            score += 1
            if score >= 1500:
                win = True  # le joueur a gagné

        # sol
        pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        # rendu
        for p in platforms:
            p.draw(screen)
        for o in obstacles:
            o.draw(screen)
        player.draw(screen)

        # affichage score
        txt = font.render(f"Score : {score}", True, TEXT_COLOR)
        screen.blit(txt, (10, 10))

        # messages de fin
        if game_over:
            over_txt = font.render("💀 Game Over ! Espace pour rejouer", True, TEXT_COLOR)
            screen.blit(over_txt, (WIDTH // 2 - 220, HEIGHT // 2 - 20))
        elif win:
            win_txt = font.render("🏁 Gagné ! Espace pour rejouer", True, TEXT_COLOR)
            screen.blit(win_txt, (WIDTH // 2 - 220, HEIGHT // 2 - 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()
