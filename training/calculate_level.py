from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

from training.creating_dataset import standardize_dataframe
import numpy as np
import pandas as pd

from training.save_load_model_to_file import load_model_from_file


def calculate_level(monster_json: str) -> str:
    model = load_model_from_file("../output/current_model.pkl")

    # Z potwora musimy wyciągnąć takie same cechy jakie mamy w X
    monster_X = pd.read_json(monster_json)
    monster_X = standardize_dataframe(monster_X)

    predict = model.predict(monster_X)
    predict = np.where(
        (predict % 1) > 0.33, np.ceil(predict), np.floor(predict)
    ).astype("int")

    if predict == 21:
        return ">20"
    return predict
