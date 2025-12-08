import pygame
import sys
import numpy as np
from config import *
from game.engine import GameEngine
from game.renderer import render
from capture.screen_capture import FrameProcessor
from IA.DQN import init_network, forward, choose_action  # à adapter à ton fichier

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash - IA Ready")
clock = pygame.time.Clock()

engine = GameEngine()
processor = FrameProcessor()

# === INITIALISATION RÉSEAU (UNE FOIS) ===
input_dim = 4 * 84 * 84
hidden1 = 128
hidden2 = 64
output_dim = 2
params = init_network(input_dim, hidden1, hidden2, output_dim)

epsilon = 0.1   # pour commencer (beaucoup d’exploration)

running = True
while running:
    dt = clock.tick(FPS)

    # Gestion des événements (fermeture fenêtre uniquement)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    # === CAPTURE POUR IA ===
    state = processor.process(screen)      # shape (4, 84, 84)
    x = state.flatten()

    # === DÉCISION IA ===
    q_values, _ = forward(params, x)      # shape (1, 2)
    q_values = q_values[0]                # shape (2,)
    action = choose_action(q_values, epsilon)

    # Traduction action → jump_pressed
    jump_pressed = (action == 1)

    # === UPDATE JEU ===
    engine.update(jump_pressed, WIDTH)

    # === RENDU ===
    render(screen, engine)
    pygame.display.flip()

pygame.quit()
sys.exit()
