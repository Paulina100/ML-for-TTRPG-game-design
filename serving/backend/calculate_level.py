import numpy as np
import pandas as pd


def calculate_level(monster_stats: dict, model) -> int:
    """
    Calculates the monster's level based on its statistics
    :param monster_stats: dict with the monster's statistics to load
    :param model: machine learning model used for prediction
    :return: int containing calculated monster's level
    """

    monster_X = pd.DataFrame.from_records([monster_stats])
    monster_y = model.predict(monster_X)
    # TODO
    monster_y = np.where(
        (monster_y % 1) > 0.33, np.ceil(monster_y), np.floor(monster_y)
    )
    monster_y = monster_y.astype("int")

    return monster_y[0]
