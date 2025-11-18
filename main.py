# main.py
import pygame
import sys
from config import *
from game.engine import GameEngine
from game.renderer import render
from capture.screen_capture import FrameProcessor

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash - IA Ready")
clock = pygame.time.Clock()

engine = GameEngine()
processor = FrameProcessor()

# === BOUCLE PRINCIPALE ===
running = True
while running:
    dt = clock.tick(FPS)
    jump_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                if engine.game_over:
                    engine.reset()
                else:
                    jump_pressed = True

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not engine.game_over:
        jump_pressed = True

    # === UPDATE ===
    engine.update(jump_pressed, WIDTH)

    # === CAPTURE POUR IA ===
    state = processor.process(screen)  # → (4, 84, 84)
    # TODO: model.predict(state) → action

    # === RENDU ===
    render(screen, engine)
    pygame.display.flip()

pygame.quit()
sys.exit()