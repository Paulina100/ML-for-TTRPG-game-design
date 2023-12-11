import os
import pathlib

from serving.backend.constants import ORDERED_CHARACTERISTICS_FULL
from training.constants import FEATURES
from training.creating_dataset import load_and_preprocess_data


current_path = os.getcwd()
DATASETS_DIR = pathlib.Path(current_path).parent / "pathfinder_2e_data"
DATASET_FILES = [
    "pathfinder-bestiary-2.db",
    "pathfinder-bestiary-3.db",
    "pathfinder-bestiary.db",
]

DATASET_PATHS = [f"{DATASETS_DIR}/{file}" for file in DATASET_FILES]

if __name__ == "__main__":
    df = load_and_preprocess_data(
        DATASET_PATHS,
        characteristics=FEATURES,
    )

    df = df[ORDERED_CHARACTERISTICS_FULL]
    df.to_csv("../counterfactual_datasets/bestiaries_full.csv")
