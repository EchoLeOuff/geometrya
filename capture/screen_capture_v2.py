# frame_processor.py
"""
FrameProcessor - Convertit l'écran Pygame en matrice de masques sémantiques

Entrée : Surface Pygame (900×500 pixels RGB)
Sortie : Matrice numpy (16, 84, 84) = 4 masques × 4 frames temporelles

Utilisation pour TIPE : Prétraitement optimisé pour réseau de neurones
exploitant les couleurs distinctes du jeu Geometry Dash recréé.
"""

import numpy as np
import pygame
import cv2
from collections import deque


class FrameProcessor:
    """
    Convertit les frames Pygame en stack de masques sémantiques temporels.
    
    Sortie : (16, 84, 84) = 4 types d'éléments × 4 frames dans le temps
    - Canal 0-3   : Frame t (la plus récente)
    - Canal 4-7   : Frame t-1
    - Canal 8-11  : Frame t-2
    - Canal 12-15 : Frame t-3 (la plus ancienne)
    
    Chaque groupe de 4 canaux contient :
    [0] joueur, [1] obstacles, [2] plateformes, [3] sol
    """
    
    def __init__(self, stack_size=4, width=84, height=84):
        """
        Paramètres :
            stack_size : Nombre de frames temporelles à conserver (défaut: 4)
            width      : Largeur de la matrice de sortie (défaut: 84)
            height     : Hauteur de la matrice de sortie (défaut: 84)
        """
        self.stack = deque(maxlen=stack_size)
        self.target_size = (width, height)
        
        # Couleurs de référence (normalisées entre 0 et 1)
        self.color_player = np.array([255, 120, 120]) / 255.0    # Rose/rouge
        self.color_obstacle = np.array([250, 210, 80]) / 255.0   # Jaune
        self.color_platform = np.array([100, 180, 255]) / 255.0  # Bleu clair
        self.color_ground = np.array([40, 40, 55]) / 255.0       # Gris foncé
        
        # Tolérance pour la détection de couleur (ajuster si nécessaire)
        self.color_tolerance = 0.15
    
    
    def process(self, screen):
        """
        Traite une frame Pygame et retourne la matrice d'état.
        
        Argument :
            screen : pygame.Surface (l'écran du jeu)
        
        Retour :
            np.ndarray de shape (16, 84, 84) et dtype float32
        """
        # Étape 1 : Conversion Pygame Surface → numpy array
        frame = pygame.surfarray.array3d(screen)     # (W, H, 3) BGR
        frame = np.transpose(frame, (1, 0, 2))       # (H, W, 3) RGB
        
        # Étape 2 : Redimensionnement à 84×84
        small = cv2.resize(frame, self.target_size, interpolation=cv2.INTER_NEAREST)
        small = small.astype(np.float32) / 255.0     # Normalisation [0, 1]
        
        # Étape 3 : Détection des 4 types d'éléments par couleur
        mask_player = self._detect_color(small, self.color_player)
        mask_obstacle = self._detect_color(small, self.color_obstacle)
        mask_platform = self._detect_color(small, self.color_platform)
        mask_ground = self._detect_color(small, self.color_ground)
        
        # Étape 4 : Empilement des 4 masques en une "frame sémantique"
        semantic_frame = np.stack([
            mask_player,
            mask_obstacle,
            mask_platform,
            mask_ground
        ], axis=0).astype(np.float32)  # Shape: (4, 84, 84)
        
        # Étape 5 : Ajout dans la pile temporelle
        self.stack.append(semantic_frame)
        
        # Étape 6 : Remplissage initial (duplication au début du jeu)
        while len(self.stack) < self.stack.maxlen:
            self.stack.append(semantic_frame)
        
        # Étape 7 : Concaténation temporelle finale
        state = np.concatenate(list(self.stack), axis=0)
        
        return state  # Shape: (16, 84, 84)
    
    
    def _detect_color(self, image, target_color):
        """
        Détecte les pixels correspondant à une couleur cible.
        
        Arguments :
            image        : Image RGB normalisée (H, W, 3)
            target_color : Couleur RGB normalisée (3,)
        
        Retour :
            Masque binaire float32 (H, W) avec 1.0 = couleur détectée
        """
        diff = np.linalg.norm(image - target_color, axis=-1)
        mask = (diff < self.color_tolerance).astype(np.float32)
        return mask
    
    
    def reset(self):
        """Vide la pile temporelle (à appeler au début de chaque épisode)."""
        self.stack.clear()
    
    
    def get_state_shape(self):
        """Retourne la forme de la matrice de sortie."""
        channels = self.stack.maxlen * 4
        h, w = self.target_size[1], self.target_size[0]
        return (channels, h, w)


# ============================================================================
# EXEMPLE D'UTILISATION (commenté)
# ============================================================================

# if __name__ == "__main__":
#     import pygame
#     
#     # Configuration
#     WIDTH, HEIGHT = 900, 500
#     BG = (25, 25, 35)
#     PLAYER_COLOR = (255, 120, 120)
#     OBSTACLE_COLOR = (250, 210, 80)
#     
#     # Initialisation Pygame
#     pygame.init()
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     
#     # Création du processeur
#     processor = FrameProcessor(stack_size=4, width=84, height=84)
#     
#     # Simulation d'une frame de jeu
#     screen.fill(BG)
#     pygame.draw.rect(screen, PLAYER_COLOR, (100, 400, 40, 40))  # Joueur
#     pygame.draw.rect(screen, OBSTACLE_COLOR, (400, 380, 30, 60)) # Obstacle
#     
#     # Génération de la matrice
#     state = processor.process(screen)
#     
#     # Vérification
#     print(f"✓ Shape de sortie : {state.shape}")
#     print(f"✓ Type : {state.dtype}")
#     print(f"✓ Min/Max : {state.min():.2f} / {state.max():.2f}")
#     print(f"✓ Pixels joueur (canal 0) : {state[0].sum():.0f}")
#     print(f"✓ Pixels obstacle (canal 1) : {state[1].sum():.0f}")
#     
#     pygame.quit()


# ============================================================================
# UTILISATION DANS TON MAIN.PY (exemple commenté)
# ============================================================================

# from frame_processor import FrameProcessor
# import pygame
# from config import *
# 
# pygame.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# clock = pygame.time.Clock()
# 
# # Initialisation
# processor = FrameProcessor()
# 
# # Boucle de jeu
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     
#     # ... ton code de jeu (déplacement joueur, obstacles, etc.) ...
#     
#     # Génération de la matrice pour l'IA
#     state = processor.process(screen)  # shape: (16, 84, 84)
#     
#     # Utilisation avec ton réseau de neurones
#     # action = neural_network.predict(state)
#     # if action == 1:
#     #     player.jump()
#     
#     pygame.display.flip()
#     clock.tick(FPS)
# 
# pygame.quit()


# ============================================================================
# UTILISATION POUR ENTRAÎNEMENT RL (exemple commenté)
# ============================================================================

# from frame_processor import FrameProcessor
# 
# processor = FrameProcessor()
# 
# # Début d'un épisode
# processor.reset()  # Vide la pile temporelle
# 
# for step in range(1000):
#     # Capture de l'état actuel
#     state = processor.process(screen)  # (16, 84, 84)
#     
#     # Décision de l'agent
#     action = agent.select_action(state)
#     
#     # Exécution de l'action dans le jeu
#     reward, done = game.step(action)
#     
#     # Capture du nouvel état
#     next_state = processor.process(screen)
#     
#     # Stockage de la transition
#     agent.store_transition(state, action, reward, next_state, done)
#     
#     if done:
#         break


# ============================================================================
# VISUALISATION DE LA MATRICE (debug - commenté)
# ============================================================================

# import matplotlib.pyplot as plt
# 
# state = processor.process(screen)
# 
# # Affichage des 4 masques de la frame la plus récente
# fig, axes = plt.subplots(1, 4, figsize=(16, 4))
# titles = ['Joueur', 'Obstacles', 'Plateformes', 'Sol']
# 
# for i in range(4):
#     axes[i].imshow(state[i], cmap='gray')
#     axes[i].set_title(titles[i])
#     axes[i].axis('off')
# 
# plt.tight_layout()
# plt.show()
