import sys

import joblib


sys.path.append("../serving/backend")
from serving.backend.calculate_level import calculate_level


def test_calculate_level():
    model = joblib.load(filename="../saved_models/current_model.pkl")

    monster_adult_white_dragon = {
        "str": 7,
        "dex": 2,
        "con": 5,
        "int": 1,
        "wis": 2,
        "cha": 1,
        "ac": 29,
        "hp": 215,
    }
    monster_lantern_archon = {
        "str": -5,
        "dex": 3,
        "con": 1,
        "int": -1,
        "wis": 1,
        "cha": 1,
        "ac": 16,
        "hp": 20,
    }
    monster_treerazer = {
        "str": 12,
        "dex": 9,
        "con": 11,
        "int": 7,
        "wis": 8,
        "cha": 8,
        "ac": 54,
        "hp": 550,
    }

    level = calculate_level(monster_stats=monster_adult_white_dragon, model=model)
    assert level in range(9, 12)

    level = calculate_level(monster_stats=monster_lantern_archon, model=model)
    assert level in range(0, 3)

    level = calculate_level(monster_stats=monster_treerazer, model=model)
    assert level in range(20, 23)
