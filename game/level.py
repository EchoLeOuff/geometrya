# game/level.py
LEVEL_DATA = [
    # Départ: quelques petits obstacles bas
    {"id": 1,  "type": "obstacle",     "x": 600},
    {"id": 2,  "type": "obstacle",     "x": 900},
    {"id": 3,  "type": "obstacle",     "x": 1200},

    # Première plateforme pour apprendre à sauter dessus
    {"id": 4,  "type": "platform",     "x": 1500, "y": 320, "width": 180},

    # Séquence de sauts au sol
    {"id": 6,  "type": "obstacle",     "x": 1950},
    {"id": 7,  "type": "obstacle",     "x": 2200},
    {"id": 8,  "type": "obstacle",     "x": 2450},

    # Deux plateformes en escalier
    {"id": 9,  "type": "platform",     "x": 2700, "y": 340, "width": 160},
    {"id": 10, "type": "obstacle", "x": 2860},
    {"id": 11, "type": "obstacle", "x": 2910},
    {"id": 12, "type": "obstacle", "x": 2960},
    {"id": 13, "type": "obstacle", "x": 3010},
    {"id": 14, "type": "obstacle", "x": 3060},
    {"id": 15, "type": "obstacle", "x": 3110},
    {"id": 16, "type": "platform",     "x": 3125, "y": 330, "width": 200},

    # Corridor de plateformes
    {"id": 17, "type": "platform",     "x": 3550, "y": 320, "width": 160},
    {"id": 18, "type": "obstacle", "x": 3710},
    {"id": 19, "type": "obstacle", "x": 3760},

    {"id": 20, "type": "platform",     "x": 3800, "y": 310, "width": 140},
    {"id": 21, "type": "obstacle", "x": 3940},
    {"id": 22, "type": "obstacle", "x": 3990},
    {"id": 23, "type": "platform",     "x": 4050, "y": 280, "width": 140},

    # Obstacles plus rapprochés
    {"id": 24, "type": "obstacle",     "x": 4350},
    {"id": 25, "type": "obstacle",     "x": 4390},

    # Grande plateforme "safe"
    {"id": 26, "type": "platform",     "x": 5050, "y": 320, "width": 300},

    # --- Rallonge du parcours ---

    # Double pic au sol
    {"id": 27, "type": "obstacle",     "x": 5450},
    {"id": 28, "type": "obstacle",     "x": 5520},

    # Petite plateforme basse puis pic
    {"id": 29, "type": "platform",     "x": 5750, "y": 340, "width": 180},
    {"id": 30, "type": "obstacle",     "x": 6020},

    # Combo: plateforme moyenne + double pic
    {"id": 31, "type": "platform",     "x": 6150, "y": 310, "width": 200},
    {"id": 32, "type": "obstacle",     "x": 6550},
    {"id": 33, "type": "obstacle",     "x": 6620},

    # Passage de précision: triple pic espacé
    {"id": 34, "type": "obstacle",     "x": 6900},
    {"id": 35, "type": "obstacle",     "x": 6950},
    {"id": 36, "type": "obstacle",     "x": 7000},

    # Plateforme haute, oblige à bien timer les sauts
    {"id": 37, "type": "platform",     "x": 7400, "y": 365, "width": 220},
    {"id": 38, "type": "obstacle",     "x": 7700},

    # Double pic juste après une plateforme
    {"id": 39, "type": "platform",     "x": 7950, "y": 320, "width": 180},
    {"id": 40, "type": "obstacle",     "x": 8220},
    {"id": 41, "type": "obstacle",     "x": 8290},

    # Final: petite série de pics + grande plateforme de fin
    {"id": 42, "type": "obstacle",     "x": 8600},
    {"id": 43, "type": "obstacle",     "x": 8645},
    {"id": 44, "type": "platform",     "x": 9100, "y": 320, "width": 380},
]
