import numpy as np
import pandas as pd

from training.creating_dataset import standardize_bestiary
from training.save_load_model_to_file import load_model_from_file


def calculate_level(monster_json: str, standardized: bool = False) -> str:
    """
    Calculates the monster's level based on its statistics
    :param monster_json: JSON string with monster's statistics to load
    :param standardized: True if given input is already standardized otherwise False
    :return: string containing calculated monster's level
    """

    model = load_model_from_file()

    monster_X = pd.read_json(monster_json, lines=True)
    if not standardized:
        monster_X = standardize_bestiary(monster_X)
        monster_X = monster_X.drop(columns=["book", "level"])

    monster_y = model.predict(monster_X)
    monster_y = np.where(
        (monster_y % 1) > 0.33, np.ceil(monster_y), np.floor(monster_y)
    ).astype("int")

    if monster_y == 21:
        return ">20"
    return str(monster_y[0])
