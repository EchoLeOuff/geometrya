# config.py
import pygame

# --- Dimensions & Physique ---
WIDTH, HEIGHT = 900, 500
FPS = 60
GRAVITY = 0.8
JUMP_VEL = -15
PLAYER_SIZE = 40
GROUND_HEIGHT = 80
OBSTACLE_SPEED = 7

# --- Couleurs ---
BG = (25, 25, 35)
GROUND_COLOR = (40, 40, 55)
PLAYER_COLOR = (255, 120, 120)
OBSTACLE_COLOR = (250, 210, 80)
PLATFORM_COLOR = (100, 180, 255)
TEXT_COLOR = (230, 230, 230)

# --- Police ---
FONT = pygame.font.Font(None, 24)