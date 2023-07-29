import joblib

from serving.backend.calculate_level import calculate_level


def test_calculate_level():
    model = joblib.load(filename="../saved_models/current_model.pkl")

    monster_adult_white_dragon = {
        "cha": 1,
        "con": 5,
        "dex": 2,
        "int": 1,
        "str": 7,
        "wis": 2,
        "ac": 29,
        "hp": 215,
    }
    monster_lantern_archon = {
        "cha": 1,
        "con": 1,
        "dex": 3,
        "int": -1,
        "str": -5,
        "wis": 1,
        "ac": 16,
        "hp": 20,
    }
    monster_treerazer = {
        "cha": 8,
        "con": 11,
        "dex": 9,
        "int": 7,
        "str": 12,
        "wis": 8,
        "ac": 54,
        "hp": 550,
    }

    level = calculate_level(monster_stats=monster_adult_white_dragon, model=model)
    assert level in range(9, 12)

    level = calculate_level(monster_stats=monster_lantern_archon, model=model)
    assert level in range(0, 3)

    level = calculate_level(monster_stats=monster_treerazer, model=model)
    assert level in range(20, 23)
