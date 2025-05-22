import pygame
import pickle
import os
import time
import matplotlib.pyplot as plt
import numpy as np
from env_platformer import PlatformerEnv
from game_config import *
from agent_qlearning import QLearningAgent

def plot_training_progress(episode_rewards):
    plt.figure(figsize=(10, 6))
    episodes = np.arange(1, len(episode_rewards) + 1)
    plt.plot(episodes, episode_rewards, 'b-', label='Average Reward per Episode')
    plt.title('Agent Training Progress')
    plt.xlabel('Episode')
    plt.ylabel('Average Reward')
    plt.grid(True)
    plt.legend()
    plt.savefig('training_progress.png')
    print("📊 Graphique sauvegardé dans 'training_progress.png'")

# Ask user for file choice
print("Voulez-vous utiliser le fichier par défaut (q_table.pkl) ou créer un nouveau fichier ?")
print("1: Fichier par défaut")
print("2: Nouveau fichier")
choice = input("Entrez votre choix (1 ou 2) : ")

if choice == "2":
    filename = input("Entrez le nom du nouveau fichier (sans extension) : ") + ".pkl"
else:
    filename = "q_table.pkl"

# Load or create Q-table
if os.path.exists(filename):
    try:
        with open(filename, "rb") as f:
            q_table = pickle.load(f)
            print(f"✅ Q-table chargée depuis {filename}. Taille: {len(q_table)} entrées")
    except Exception as e:
        print(f"⚠️ Erreur lors du chargement de {filename}: {e}")
        print("Création d'une nouvelle Q-table")
        q_table = {}
else:
    print(f"⚠️ Fichier {filename} non trouvé. Création d'un nouveau fichier.")
    q_table = {}
    try:
        with open(filename, "wb") as f:
            pickle.dump(q_table, f) 
        print(f"✅ Nouveau fichier {filename} créé.")
    except Exception as e:
        print(f"❌ Erreur lors de la création de {filename}: {e}")

# Ask user for rendering choice
print("Voulez-vous activer le rendu graphique pendant l'entraînement ? (Cela peut ralentir l'exécution)")
print("1: Oui (afficher les 4 sessions)")
print("2: Non (entraînement sans rendu)")
render_choice = input("Entrez votre choix (1 ou 2) : ")
render_training = render_choice == "1"

# Create shared screen for 2x2 grid if rendering
if render_training:
    pygame.init()
    screen_width, screen_height = WIDTH * 2, HEIGHT * 2
    screen = pygame.display.set_mode((screen_width, screen_height))
else:
    screen = None

# Create four environments with offsets for 2x2 grid
num_sessions = 4
offsets = [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]
envs = [PlatformerEnv(render_mode=render_training, screen=screen, offset_x=ox, offset_y=oy) for (ox, oy) in offsets]
agents = [QLearningAgent(actions=[0, 1], alpha=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01) for _ in range(num_sessions)]
for agent in agents:
    agent.q_table = q_table

# Training phase
num_episodes = 100
max_steps_per_episode = 500
print("🚀 Début de l'entraînement avec 4 sessions parallèles...")
episode_rewards = []
for episode in range(num_episodes):
    observations = [env.reset() for env in envs]
    dones = [False] * num_sessions
    ep_rewards = [0] * num_sessions
    step_count = 0
    while not all(dones) and step_count < max_steps_per_episode:
        for i in range(num_sessions):
            if not dones[i]:
                action = agents[i].choose_action(observations[i], explore=True)
                next_obs, reward, dones[i], _ = envs[i].step(action)
                agents[i].learn(observations[i], action, reward, next_obs)
                observations[i] = next_obs
                ep_rewards[i] += reward
        if render_training:
            screen.fill((0, 0, 0))
            for env in envs:
                env.render()
            time.sleep(0.002)
        step_count += 1
    avg_reward = sum(ep_rewards) / num_sessions
    episode_rewards.append(avg_reward)
    print(f"Épisode {episode + 1}/{num_episodes}, Récompense moyenne: {avg_reward:.2f}, Epsilon: {agents[0].epsilon:.3f}, Taille Q-table: {len(q_table)}")

# Plot training progress
plot_training_progress(episode_rewards)

# Save Q-table after training
try:
    with open(filename, "wb") as f:
        pickle.dump(q_table, f)
        print(f"✅ Q-table sauvegardée dans {filename}. Taille: {len(q_table)} entrées")
except Exception as e:
    print(f"❌ Erreur lors de la sauvegarde de la Q-table: {e}")

# Testing phase with first environment
print("🧪 Début du test...")
pygame.display.set_mode((WIDTH, HEIGHT))
envs[0].screen = pygame.display.get_surface()
envs[0].offset_x, envs[0].offset_y = 0, 0
envs[0].render_mode = True
obs = envs[0].reset()
done = False
total_reward = 0
frame_delay = 0.03

while not done:
    action = agents[0].choose_action(obs, explore=False)
    obs, reward, done, _ = envs[0].step(action)
    total_reward += reward
    envs[0].render()
    time.sleep(frame_delay)

# Save Q-table again after testing
try:
    with open(filename, "wb") as f:
        pickle.dump(q_table, f)
        print(f"✅ Q-table sauvegardée dans {filename}. Taille: {len(q_table)} entrées")
except Exception as e:
    print(f"❌ Erreur lors de la sauvegarde de la Q-table: {e}")

print(f"🏁 Test terminé. Récompense totale : {total_reward:.2f}")
for env in envs:
    env.close()