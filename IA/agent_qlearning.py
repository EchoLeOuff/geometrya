import random

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, jump_probability=0.1):
        self.q_table = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.jump_probability = jump_probability  # Nouvelle variable pour contrôler la fréquence des sauts

    def _state_to_key(self, state):
        return tuple(round(x, 3) if isinstance(x, float) else x for x in state)

    def get_q(self, state, action):
        state = self._state_to_key(state)
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state, explore=True):
        state = self._state_to_key(state)
        if explore and random.random() < self.epsilon:
            # Ajuster la probabilité de choisir l'action "sauter"
            if "sauter" in self.actions:
                # Créer une liste de probabilités personnalisées
                probabilities = [self.jump_probability if action == "sauter" else (1 - self.jump_probability)/(len(self.actions) - 1) for action in self.actions]
                return random.choices(self.actions, probabilities, k=1)[0]
            else:
                return random.choice(self.actions)
        q_vals = [self.get_q(state, a) for a in self.actions]
        max_q = max(q_vals)
        best_actions = [self.actions[i] for i, q in enumerate(q_vals) if q == max_q]
        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state):
        state = self._state_to_key(state)
        next_state = self._state_to_key(next_state)
        max_next_q = max([self.get_q(next_state, a) for a in self.actions])
        current_q = self.get_q(state, action)
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[(state, action)] = new_q
        self.update_epsilon()

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)