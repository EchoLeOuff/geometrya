import numpy as np
import random

# ============================================================
# 1) Initialisation du réseau
# ============================================================

def init_network(input_dim, hidden1, hidden2, output_dim):
    params = {}

    params["W1"] = np.random.randn(hidden1, input_dim) * np.sqrt(2. / input_dim)
    params["b1"] = np.zeros(hidden1)

    params["W2"] = np.random.randn(hidden2, hidden1) * np.sqrt(2. / hidden1)
    params["b2"] = np.zeros(hidden2)

    params["W3"] = np.random.randn(output_dim, hidden2) * np.sqrt(2. / hidden2)
    params["b3"] = np.zeros(output_dim)

    return params


# ============================================================
# 2) Fonctions utilitaires : ReLU + dérivée
# ============================================================

def relu(z):
    return np.maximum(0, z)

def relu_derivative(z):
    return (z > 0).astype(np.float32)


# ============================================================
# 3) Forward (1 seul état ou batch)
# ============================================================

def forward(params, X):
    """
    X : shape (input_dim,) OU (batch_size, input_dim)
    Retourne :
        Q_values : shape (2,) OU (batch_size, 2)
        cache : objets nécessaires pour le backward
    """
    if X.ndim == 1:
        X = X.reshape(1, -1)
    
    is_batch = (X.ndim == 2)

    # 1) Couche 1
    z1 = X @ params["W1"].T + params["b1"]
    h1 = relu(z1)

    # 2) Couche 2
    z2 = h1 @ params["W2"].T + params["b2"]
    h2 = relu(z2)

    # 3) Couche de sortie
    q = h2 @ params["W3"].T + params["b3"]

    cache = (X, z1, h1, z2, h2)

    return q, cache

# ============================================================
# 4) Choix d’action (epsilon-greedy)
# ============================================================

def choose_action(Q_values, epsilon):
    if random.random() < epsilon:
        return random.randint(0, len(Q_values) - 1)
    return int(np.argmax(Q_values))


# ============================================================
# 5) Replay Buffer
# ============================================================

def store_transition(buffer, state, action, reward, next_state, done):
    buffer.append((state, action, reward, next_state, done))

def sample_batch(buffer, batch_size):
    batch = random.sample(buffer, min(batch_size, len(buffer)))
    
    states, actions, rewards, next_states, dones = zip(*batch)

    states      = np.array([s.flatten() for s in states],      dtype=np.float32)
    next_states = np.array([s.flatten() for s in next_states], dtype=np.float32)
    actions     = np.array(actions,  dtype=np.int64)
    rewards     = np.array(rewards,  dtype=np.float32)
    dones       = np.array(dones,    dtype=np.float32)

    return states, actions, rewards, next_states, dones


# ============================================================
# 6) Calcul des cibles Q-learning
# ============================================================

def compute_targets(params, rewards, next_states, dones, gamma):
    batch_size = rewards.shape[0]

    # Q(next_state, •)
    q_next, _ = forward(params, next_states)

    # max_a' Q(next_state, a')
    max_q_next = np.max(q_next, axis=1)

    # y = r si done, sinon r + gamma * maxQ
    targets = rewards + (1 - dones) * gamma * max_q_next

    return targets


# ============================================================
# 7) Backward : rétropropagation
# ============================================================

def backward(params, cache, actions, targets):
    """
    cache : (X, z1, h1, z2, h2)
    actions : (B,)
    targets : (B,)
    """

    X, z1, h1, z2, h2 = cache
    batch_size = X.shape[0]

    # --------------------------------------------------------
    # Forward final : Q(s)
    # --------------------------------------------------------
    q_pred = h2 @ params["W3"].T + params["b3"]  # (B,2)

    # Erreur uniquement sur les actions prises
    diff = q_pred[np.arange(batch_size), actions] - targets  # (B,)

    # Gradient Q-layer
    dq = np.zeros_like(q_pred)
    dq[np.arange(batch_size), actions] = diff * 2.0 / batch_size

    # --------------------------------------------------------
    # dW3, db3
    # --------------------------------------------------------
    dW3 = dq.T @ h2        # (2,64)
    db3 = dq.sum(axis=0)   # (2,)

    # --------------------------------------------------------
    # Backprop vers h2
    # --------------------------------------------------------
    dh2 = dq @ params["W3"]    # (B,64)
    dz2 = dh2 * relu_derivative(z2)

    # dW2, db2
    dW2 = dz2.T @ h1
    db2 = dz2.sum(axis=0)

    # Backprop vers h1
    dh1 = dz2 @ params["W2"]
    dz1 = dh1 * relu_derivative(z1)

    # dW1, db1
    dW1 = dz1.T @ X
    db1 = dz1.sum(axis=0)

    grads = {
        "W1": dW1, "b1": db1,
        "W2": dW2, "b2": db2,
        "W3": dW3, "b3": db3
    }
    return grads


# ============================================================
# 8) Mise à jour des paramètres
# ============================================================

def update_params(params, grads, lr):
    # --- AJOUT : Gradient Clipping ---
    max_norm = 1.0 
    for key in grads:
        # Si le gradient est trop grand, on le réduit proportionnellement
        norm = np.linalg.norm(grads[key])
        if norm > max_norm:
            grads[key] = grads[key] * (max_norm / norm)
    # ---------------------------------
    
    for key in params.keys():
        params[key] -= lr * grads[key]