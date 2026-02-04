# Projet TIPE GeometrIA

## 📖 Présentation

À travers l'exemple d'un jeu vidéo (_**Geometry Dash**_), nous allons montrer comment on peut optimiser un modèle afin de réussir un niveau.

_**Geometry Dash**_ est une course d’obstacles. Il n’y a qu’une seule commande : **sauter**. Le but est d’esquiver des **piques** et des **blocs**, puis de finir la course.

Ainsi, nous implémenterons un réseau de trois neurones :
1. Un qui détecte s’il y a un **bloc**,

2. Un qui détecte s’il y a un **pique**,

3. Et le dernier qui **active le saut**.

Ensuite, nous lancerons la première génération de parties (1 000 parties), où le programme va positionner aléatoirement ses neurones. Parmi ces 1 000 parties, nous garderons celle où le personnage est allé le plus loin dans la course. À partir de celle-ci, nous générerons 1 000 nouvelles parties où la position des neurones sera générée à partir de la meilleure partie de la génération précédente.

Une fois le niveau complété, nous obtiendrons notre IA « témoin », qui se sera **entraînée toute seule**.

Enfin, nous générerons d’autres simulations en ajoutant des conditions initiales sur le positionnement des neurones, dans le but de **réduire au maximum le nombre de générations nécessaires**.

## 📂 Architecture du Git


## 🔎 Bilan du Sprint 1

### 🛠 Conception d’un Niveau Simplifié
Nous avons commencé par développer une version simplifiée du jeu en Python.
Le but est de créer un environnement contrôlé pour entraîner l’IA.

➡️ **À ce stade, seules les mécaniques de base** (saut, déplacement, gestion des collisions) ont été implémentées.
Un **niveau jouable complet n’est pas encore disponible**.

### 🧠 Exploration des Approches Machine Learning
Nous avons exploré la piste du reinforcement learning avec PyTorch, en étudiant notamment deux algorithmes :

- **DQN (Deep Q-Network)** : apprentissage d’une fonction de valeur Q.

- **PPO (Proximal Policy Optimization)** : plus stable pour l’entraînement d’agents RL.

### 👥 Répartition des Rôles et Tâches

|   Période   | Tâche                               |Responsable |
| ----------- | ----------------------------------- |------------|
| Semaine 1-2 | Recherche sur ML et Pytorch         | Dorian     |
| Semaine 1-2 | Modélisation des mécaniques de jeux | Vincent    |

### 📚 Ressources Consultées
- Articles sur **DQN** (Mnih et al., 2015) et **PPO** (Schulman et al., 2017).

- **Documentation officielle PyTorch** (modules torch.nn, torch.optim, etc.).

- Tutoriels “Reinforcement Learning” du site officiel PyTorch.

- Exemples d’agents IA jouant à des jeux 2D.


> ⚠️ La documentation est dense et parfois difficile à aborder au départ.
Nous avons pris le temps de clarifier certains concepts clés avant d’implémenter quoi que ce soit.

### ✅ Solutions Envisagées / Réalisées 

| Solution             | Statut            | Description courte                                                |
| -------------------- | ----------------- | ----------------------------------------------------------------- |
| CNN pour détection   | Documentation     | Réseau de convultion repérage d'obstacle                          |
| Agent DQN en PyTorch | En test           | Agent RL (reinforcement learning) déscisionnaire des actions      |
| Simulation Python    | Mécaniques codées | Implémentation des bases du jeu mais pas encore de niveau jouable |

### ⚠️ Difficultés et Obstacles

| Difficulté                               | Solution adoptée                                                     |
| ---------------------------------------- | -------------------------------------------------------------------- |
| Compréhension des concepts RL et PyTorch | Lecture d’articles, tutoriels, documentation officielle              |
| Densité de la documentation PyTorch      | Nécessite du temps pour appropriation ; beaucoup de jargon technique |
| Coordination entre les tâches	           | Mise en place de réunions rapides pour synchroniser les avancées     |

### 📌 Conclusion et Perspectives

✅ **Avancement actuel :**
- Mécaniques de jeu codées.

- Connaissances théoriques solides sur les algorithmes DQN et PPO.

- Répartition claire des tâches.

🔜 **À venir :**
- **Implémenter un niveau jouable** pour que l’agent puisse commencer à s’entraîner.

- **Débuter l’architecture du réseau de neurones** (DQN).

- **Lancer les premiers tests d’entraînement IA.**

## 🔎 Bilan du Sprint 2

### 🛠 Conception du premier modèle en Q-Learning
Nous avons poursuivie le développement de notre version simplifiée du jeu en Python.
Puis création du premier modèle d'apprentissage.

➡️ **À ce stade, le niveau reste incomplet et le premier modèle possède encore des axes d'amélioration**, le q-learning est fonctionnel.

**Q-learning** : algorithme d'apprentissage par renforcement avec un système de récompense. 

### 🧠 Exploration des Approches Machine Learning
Nous avons continuer à étudier les différentes solution de machine learning en python adapté à nos besoins.


### 👥 Répartition des Rôles et Tâches

|   Période   | Tâche                                                    |Responsable |
| ----------- | ---------------------------------------------------------|------------|
| Semaine 3-4 | approfondissement des recherches sur le machine learning | Vincent    |
| Semaine 3-4 | ajout de l'algorithme d'apprentissage par renforcement   | Dorian     |

### 📚 Ressources Consultées
- vidéo youtube de CODE BH - J'ai fait une IA qui apprend à jouer à Geometry Dash.
- vidéo youtube de Thibault Neveu - Apprentissage par renforcement #7 : Deep Q-Learning, apprendre à conduire
- vidéo youtube de Siraj Raval - Q Learning Explained (tutorial)
- Exemples d’agents IA jouant à des jeux 2D.


### ✅ Solutions Envisagées / Réalisées 

| Solution             | Statut            | Description courte                                                 |
| -------------------- | ----------------- | -----------------------------------------------------------------  |
| Agent Q-learning     | Opérationnels     | Agent fonctionnelle. Entrainement impossible sans la fin du niveau |
| Simulation Python    | Mécaniques codées | Méchaniques opérationnelles.                                       |
| Niveau               | en cours          | Niveau icomplet qui permet pas encore un apprentissage interessant |

### ⚠️ Difficultés et Obstacles

| Difficulté                               | Solution adoptée                                                           |
| ---------------------------------------- | -------------------------------------------------------------------------- |
| Organisation du code                     | on s'est mit d'accord sur les bibliothèque a utiliser et nettoyage du code |

### 📌 Conclusion et Perspectives

✅ **Avancement actuel :**
- Mécaniques de jeu codées et fonctionnelles.

- Réorganisation du code afin d'avoir une meilleur visibilité.

- Ajout de l'agent de Q-learning. 



🔜 **À venir :**
- **Créer un niveau complet** pour commencer l'entrainement.
- **Lancer les premiers tests d’entraînement IA.**

## 🚀 Installation rapide

### Prérequis
- Python 3.11+ (vérifiez avec `python3 --version`)
- Poetry (installez avec `curl -sSL https://install.python-poetry.org | python3 -`)

### Étapes
1. Clonez le repo :
```bash
git clone https://github.com/tonuser/geometrya.git
cd geometrya
```

2. Installez les dépendances (crée l'environnement virtuel automatiquement) :

```bash
poetry install --no-root
```
4. Activez l'environnement :

```bash
eval "$(poetry env activate --shell bash)"  # ou fish: eval (poetry env activate --shell fish)
```
si cela ne fonctionne pas : 

```bash
$ eval $(poetry env activate)
```

5. Lancez vos scripts :

```bash
poetry install --no-root  # Une fois au clean (dépendances)
poetry run python train.py # À chaque exécution (training DQN)
```
