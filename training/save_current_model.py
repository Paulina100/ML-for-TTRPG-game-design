import pathlib

import joblib

from serving.backend.constants import ORDERED_CHARACTERISTICS
from training.create_model import get_fitted_model
from training.creating_dataset import load_and_preprocess_data


if __name__ == "__main__":
    DATASETS_DIR = pathlib.Path(__file__).parent.parent / "pathfinder_2e_data"
    DATASET_FILES = [
        "abomination-vaults-bestiary.db",
        "age-of-ashes-bestiary.db",
        "agents-of-edgewatch-bestiary.db",
        "april-fools-bestiary.db",
        "blog-bestiary.db",
        "blood-lords-bestiary.db",
        "book-of-the-dead-bestiary.db",
        "crown-of-the-kobold-king-bestiary.db",
        "extinction-curse-bestiary.db",
        "fall-of-plaguestone.db",
        "fists-of-the-ruby-phoenix-bestiary.db",
        "gatewalkers-bestiary.db",
        "impossible-lands-bestiary.db",
        "kingmaker-bestiary.db",
        "malevolence-bestiary.db",
        "menace-under-otari-bestiary.db",
        "monsters-of-myth-bestiary.db",
        "mwangi-expanse-bestiary.db",
        "night-of-the-gray-death-bestiary.db",
        "npc-gallery.db",
        "one-shot-bestiary.db",
        "outlaws-of-alkenstar-bestiary.db",
        "pathfinder-bestiary-2.db",
        "pathfinder-bestiary-3.db",
        "pathfinder-bestiary.db",
        "pathfinder-dark-archive.db",
        "pfs-introductions-bestiary.db",
        "pfs-season-1-bestiary.db",
        "pfs-season-2-bestiary.db",
        "pfs-season-3-bestiary.db",
        "pfs-season-4-bestiary.db",
        "quest-for-the-frozen-flame-bestiary.db",
        "shadows-at-sundown-bestiary.db",
        "strength-of-thousands-bestiary.db",
        "the-slithering-bestiary.db",
        "travel-guide-bestiary.db",
        "troubles-in-otari-bestiary.db",
    ]
    DATASET_PATHS = [f"{DATASETS_DIR}/{file}" for file in DATASET_FILES]

    X = load_and_preprocess_data(
        DATASET_PATHS,
        characteristics=ORDERED_CHARACTERISTICS,
    )
    X.pop("book")
    y = X.pop("level")
    X = X[ORDERED_CHARACTERISTICS]

    lightgbm = get_fitted_model(classifier_name="lightgbm", X_train=X, y_train=y)

    joblib.dump(value=lightgbm, filename="../saved_models/current_model.pkl")
