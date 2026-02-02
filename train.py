# train.py
import time
import numpy as np
import pygame
from config import *
from game.engine import GameEngine
from game.renderer import *
from capture.screen_capture import FrameProcessor
from IA.DQN import (
    init_network, forward, choose_action,
    store_transition, sample_batch,
    compute_targets, backward, update_params
)
import matplotlib.pyplot as plt


def make_env():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Geometry Dash - DQN Training")
    clock = pygame.time.Clock()
    engine = GameEngine()
    processor = FrameProcessor()
    return screen, clock, engine, processor


def reset_env(screen, engine, processor, clock):
    engine.reset()
    screen.fill(BG)
    pygame.display.flip()
    state = processor.process(screen)  # (4, 84, 84)
    return state


def step_env(screen, engine, processor, clock, action):
    jump_pressed = (action == 1)

    # Limitation FPS + mesure du temps entre frames
    clock.tick(FPS)

    engine.update(jump_pressed, WIDTH)
    render(screen, engine)
    pygame.display.flip()

    # Récompense très simple (à ajuster)
    reward = 1.0
    done = engine.game_over
    if done:
        reward = -10.0

    state = processor.process(screen)
    return state, reward, done


def train_dqn(
    num_episodes=10,
    batch_size=32,
    gamma=0.99,
    lr=1e-3,
    save_path="params_dqn.npy"
):
    screen, clock, engine, processor = make_env()

    input_dim = 4 * 84 * 84
    params = init_network(input_dim, 128, 64, 2)

    replay_buffer = []

    epsilon = 1.0
    epsilon_min = 0.1
    epsilon_decay = 0.995

    # Pour les courbes
    episodic_rewards = []
    episodic_durations = []      # temps (s) par épisode
    episodic_fps = []            # FPS moyen par épisode
    episodic_efficiency = []     # reward / seconde

    for ep in range(num_episodes):
        state = reset_env(screen, engine, processor, clock)
        done = False
        total_reward = 0.0

        # métriques temporelles par épisode
        start_time = time.time()
        frame_count = 0

        while not done:
            # Gestion fermeture fenêtre
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # État → Q → action
            x = state.flatten()[None, :]           # (1, input_dim)
            q_values, _ = forward(params, x)       # (1, 2)
            action = choose_action(q_values[0], epsilon)

            # Step env
            next_state, reward, done = step_env(screen, engine, processor, clock, action)

            # Stockage transition
            store_transition(replay_buffer, state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            frame_count += 1

            # Apprentissage
            if len(replay_buffer) >= batch_size:
                states, actions, rewards, next_states, dones = sample_batch(replay_buffer, batch_size)
                targets = compute_targets(params, rewards, next_states, dones, gamma)
                q_pred, cache = forward(params, states)
                grads = backward(params, cache, actions, targets)
                update_params(params, grads, lr)

        # Fin épisode : métriques
        duration = time.time() - start_time
        avg_fps = frame_count / duration if duration > 0 else 0.0
        efficiency = total_reward / duration if duration > 0 else 0.0

        episodic_rewards.append(total_reward)
        episodic_durations.append(duration)
        episodic_fps.append(avg_fps)
        episodic_efficiency.append(efficiency)

        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        print(
            f"Episode {ep+1}/{num_episodes} | "
            f"Reward={total_reward:.1f} | "
            f"epsilon={epsilon:.3f} | "
            f"frames={frame_count} | "
            f"time={duration:.2f}s | "
            f"FPS_moy={avg_fps:.1f} | "
            f"reward/s={efficiency:.2f}"
        )

    # === SAUVEGARDE DES PARAMS ===
    np.save(save_path, params, allow_pickle=True)
    print(f"Paramètres sauvegardés dans {save_path}")

    # === COURBES ===
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 2, 1)
    plt.plot(episodic_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Total reward")
    plt.title("Reward par épisode")
    plt.grid()

    plt.subplot(2, 2, 2)
    plt.plot(episodic_durations)
    plt.xlabel("Episode")
    plt.ylabel("Durée (s)")
    plt.title("Durée par épisode")
    plt.grid()

    plt.subplot(2, 2, 3)
    plt.plot(episodic_fps)
    plt.xlabel("Episode")
    plt.ylabel("FPS moyen")
    plt.title("FPS moyen par épisode")
    plt.grid()

    plt.subplot(2, 2, 4)
    plt.plot(episodic_efficiency)
    plt.xlabel("Episode")
    plt.ylabel("Reward / s")
    plt.title("Efficacité (reward par seconde)")
    plt.grid()

    plt.tight_layout()
    plt.savefig("training_metrics.png")
    plt.show()

    pygame.quit()


if __name__ == "__main__":
    train_dqn()
