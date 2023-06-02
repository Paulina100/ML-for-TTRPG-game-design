import os.path
import pathlib
from copy import deepcopy

import pandas as pd

from training.analysis_functions import get_merged_bestiaries, unpack_column_with_null


DATASETS_DIR = pathlib.Path(__file__).parent.parent / "pathfinder_2e_data"
DATASET_FILES = [
    "pathfinder-bestiary.db",
    "pathfinder-bestiary-2.db",
    "pathfinder-bestiary-3.db",
]
DATASET_PATHS = [f"{DATASETS_DIR}/{file}" for file in DATASET_FILES]
VALUE_TO_LOAD = {
    "system/abilities": "mod",
    "system/attributes/ac": "value",
    "system/attributes/hp": "value",
    "system/attributes/perception": "value",
    "system/saves": "value",
    "system/saves/fortitude": "value",
    "system/saves/reflex": "value",
    "system/saves/will": "value",
    "system/resources/focus": "value",
    "system/details/level": "value",
    "system/details/source": "value",
}


def is_path_correct(path: str) -> bool:
    """
    Checks whether given path is correct: file exists and correct file extension - json or db

    :param path: path to book to load
    :return: True if path is correct otherwise False
    """
    if not os.path.isfile(path):
        print(f"Path {path} does not exist")
        return False
    if not (path.endswith(".db") or path.endswith(".json")):
        print(f"Expected db or json file, got {path}")
        return False
    return True


def get_subcolumn(book: pd.DataFrame, subcolumn_path: str) -> pd.DataFrame:
    """
    Gets subcolumn of given DataFrame according to given path or one level up column in the path if it is known that the next colum have missing data

    :param book: DataFrame with all data from book(s)
    :param subcolumn_path: path to subcolumn
    :return: chosen subcolumn as DataFrame
    """
    subcol = deepcopy(book)
    for col in subcolumn_path.split("/"):
        subcol = pd.DataFrame(data=unpack_column_with_null(subcol, col))

    return subcol


def load_bestiaries_from_paths(
    paths_to_books: list[str] = DATASET_PATHS,
) -> pd.DataFrame:
    """
    Loads bestiaries from given paths to one DataFrame

    :param paths_to_books: list of paths of books to load
    :return: Dataframe with loaded bestiaries from given paths
    """
    for i in range(len(paths_to_books) - 1, -1, -1):
        if not is_path_correct(paths_to_books[i]):
            paths_to_books.pop(i)

    return get_merged_bestiaries(paths_to_books)


def get_column_name(characteristic: str):
    """
    Returns name for a given characteristic

    :param characteristic: characteristic in a form of path
    :return: name for a given characteristic
    """
    if characteristic == "system/details/source":
        return "book"
    return characteristic.split("/")[
        -1
    ]  # it is usually the last part of "path to characteristic"


def gat_all_characteristics(characteristics: list[str]):
    """
    Creates list with given characteristics and basic ones that always have to be included

    :param characteristics: list of characteristics
    :return: list of all characteristics to load
    """
    return characteristics + [
        i
        for i in ["system/details/level", "system/details/source"]
        if i not in characteristics
    ]


def load_and_preprocess_data(
    paths_to_books: list[str] = DATASET_PATHS,
    characteristics: list[str] = [
        "system/abilities",
        "system/attributes/ac",
        "system/attributes/hp",
    ],
) -> pd.DataFrame:
    """
    Creates dataframe containing chosen characteristics, level (CR) and source book of monsters from chosen books

    :param paths_to_books: list of paths of books to load
    :param characteristics: list of characteristics to load
    :return: DataFrame with monsters (NPC) from chosen books and with chosen characteristics and their origin book
    """

    bestiary = load_bestiaries_from_paths(paths_to_books)
    bestiary = bestiary[bestiary["type"] == "npc"]

    subcolumns = []
    for characteristic in gat_all_characteristics(characteristics):
        original_column_name = VALUE_TO_LOAD.get(characteristic)
        # get original column name of value
        # also used to check if feature is supported

        if not original_column_name:
            raise ValueError(f"Subcolumn {characteristic} does not exists")

        subcolumn = get_subcolumn(bestiary, characteristic)

        if characteristic in ["system/abilities", "system/saves"]:
            # different way of getting features than others
            # group of features instead of only one
            subcolumn = subcolumn.applymap(
                lambda x: x.get(VALUE_TO_LOAD.get(characteristic)), na_action="ignore"
            )
        else:
            column_name = get_column_name(characteristic)
            original_column_name = VALUE_TO_LOAD.get(characteristic)

            subcolumn = subcolumn[original_column_name].rename(column_name)

            if column_name == "focus":
                subcolumn = subcolumn.fillna(-1)

        subcolumns.append(subcolumn)
    df = pd.concat(subcolumns, axis=1)
    df.loc[df["level"] > 20, "level"] = 21
    return df
