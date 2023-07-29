import pathlib

import joblib

from training.create_model import get_fitted_model
from training.creating_dataset import load_and_preprocess_data


if __name__ == "__main__":
    DATASETS_DIR = pathlib.Path(__file__).parent.parent / "pathfinder_2e_data"
    DATASET_FILES = [
        "pathfinder-bestiary.db",
        "pathfinder-bestiary-2.db",
        "pathfinder-bestiary-3.db",
    ]
    DATASET_PATHS = [f"{DATASETS_DIR}/{file}" for file in DATASET_FILES]

    X = load_and_preprocess_data(
        DATASET_PATHS,
        characteristics=[
            "cha",
            "con",
            "dex",
            "int",
            "str",
            "wis",
            "ac",
            "hp",
            "focus",
            "fortitude",
        ],
    )
    X.pop("book")
    y = X.pop("level")
    rf = get_fitted_model(classifier_name="random_forest", X_train=X, y_train=y)

    joblib.dump(value=rf, filename="../saved_models/current_model.pkl")
