import os
import pathlib

import joblib

from serving.backend.calculate_level import calculate_level
from serving.backend.generate_counterfactuals import generate_counterfactuals
from training.creating_dataset import load_and_preprocess_data


current_path = os.getcwd()
DATASETS_DIR = pathlib.Path(current_path).parent / "pathfinder_2e_data"
DATASET_FILES = [
    "pathfinder-bestiary.db",
    "pathfinder-bestiary-2.db",
    "pathfinder-bestiary-3.db",
]
DATASET_PATHS = [f"{DATASETS_DIR}/{file}" for file in DATASET_FILES]
characteristics = [
    "cha",
    "con",
    "dex",
    "int",
    "str",
    "wis",
    "ac",
    "hp",
]

df = load_and_preprocess_data(
    DATASET_PATHS,
    characteristics=characteristics,
)


def test_generate_counterfactuals():
    def check_cfs(monster, cfs, new_level):
        for cf_nr in range(len(cfs["values"])):
            test_monster = {}
            for i, val in enumerate(monster.items()):
                if cfs["modified"][cf_nr][i]:
                    assert cfs["values"][cf_nr][i] != val[1]
                else:
                    assert cfs["values"][cf_nr][i] == val[1]
                test_monster[val[0]] = cfs["values"][cf_nr][i]
            assert calculate_level(test_monster, model) == new_level

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
    new_level = level - 1
    cfs = generate_counterfactuals(
        monster_stats=monster_adult_white_dragon,
        model=model,
        new_level=new_level,
        df=df,
        total_cf=3,
    )
    check_cfs(monster_adult_white_dragon, cfs, new_level)

    level = calculate_level(monster_stats=monster_lantern_archon, model=model)
    new_level = level + 1
    cfs = generate_counterfactuals(
        monster_stats=monster_lantern_archon, model=model, new_level=new_level, df=df
    )
    check_cfs(monster_lantern_archon, cfs, new_level)

    level = calculate_level(monster_stats=monster_treerazer, model=model)
    new_level = 17
    cfs = generate_counterfactuals(
        monster_stats=monster_treerazer, model=model, new_level=new_level, df=df
    )
    check_cfs(monster_treerazer, cfs, new_level)
