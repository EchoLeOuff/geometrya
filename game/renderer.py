# game/renderer.py
import pygame
from config import *

def render(screen, engine):
    screen.fill(BG)

    # Sol
    pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

    # Entités
    for p in engine.platforms:
        p.draw(screen)
    for o in engine.obstacles:
        o.draw(screen)
    engine.player.draw(screen)

    # Score
    txt = FONT.render(f"Score : {engine.score}", True, TEXT_COLOR)
    screen.blit(txt, (10, 10))

    # Game Over
    if engine.game_over:
        over_txt = FONT.render("Game Over ! Espace pour rejouer", True, TEXT_COLOR)
        screen.blit(over_txt, (WIDTH // 2 - 200, HEIGHT // 2 - 20))