import json
import os.path
import pathlib

import pandas as pd


DATASETS_DIR = pathlib.Path(__file__).parent.parent / "pathfinder_2e_data"
DATASET_FILES = [
    "pathfinder-bestiary.db",
    "pathfinder-bestiary-2.db",
    "pathfinder-bestiary-3.db",
]
DATASET_PATHS = [f"{DATASETS_DIR}/{file}" for file in DATASET_FILES]

CHARACTERISTICS_COLUMNS = {
    # "abilities": "abilities",
    "cha": "abilities.cha.mod",
    "con": "abilities.con.mod",
    "mod": "abilities.dex.mod",
    "int": "abilities.int.mod",
    "str": "abilities.str.mod",
    "wis": "abilities.wis.mod",
    "ac": "attributes.ac.value",
    "hp": "attributes.hp.value",
    "perception": "attributes.perception.value",
    # "saves": "saves"
    "fortitude": "saves.fortitude.value",
    "reflex": "saves.reflex.value",
    "will": "saves.will.value",
    "focus": "resources.focus.value",
    "level": "details.level.value",
    "book": "details.source.value",
}
"""dictionary with characteristics names (keys) and "path" to real columns in dataframe loaded from file (values)"""


def is_path_correct(path: str) -> bool:
    """
    Checks whether given path is correct: file exists and correct file extension - json or db

    :param path: path to book to load
    :return: True if path is correct
    """
    if not os.path.isfile(path):
        raise ValueError(f"Path {path} does not exist")
        # return False
    if not (path.endswith(".db") or path.endswith(".json")):
        raise ValueError(f"Expected db or json file, got {path}")
        # return False
    return True


def load_and_preprocess_data(
    paths_to_books: list[str] = None,
    characteristics: list[str] = None,
) -> pd.DataFrame:
    """
    Creates dataframe containing chosen characteristics, level and source book of monsters from chosen books

    :param paths_to_books: list of paths of books to load
    :param characteristics: list of characteristics to load
    :return: DataFrame with monsters (NPC) from chosen books and with chosen characteristics and their origin book
    """

    if paths_to_books is None:
        paths_to_books = DATASET_PATHS

    if characteristics is None:
        characteristics = ["abilities", "ac", "hp"]

    data = []

    for path in paths_to_books:
        is_path_correct(path)
        with open(path) as file:
            # loading json strings from files
            d = [json.loads(line) for line in file]
            # getting only system column (all characteristics are there)
            # getting only npc - monsters
            data += [line.get("system") for line in d if line.get("type") == "npc"]
            file.close()

    bestiary = pd.json_normalize(data)

    columns = []
    for characteristic in set(characteristics + ["book", "level"]):
        # different way of loading data: abilities and saves is a group of characteristics
        if characteristic in ["abilities", "saves"]:
            subcolumns = bestiary.filter(regex=characteristic)

            # in case of saves we have to filter to extract only useful columns
            if characteristic == "saves":
                subcolumns = subcolumns.filter(regex="value")

            # renaming columns to simpler names of characteristics
            subcolumns = subcolumns.rename(
                columns={col: col.split(".")[-2] for col in subcolumns.columns}
            )
            columns.append(subcolumns)
            continue
        # renaming the column to a simpler name of characteristic
        column = bestiary[CHARACTERISTICS_COLUMNS.get(characteristic)].rename(
            characteristic
        )
        columns.append(column)

    df = pd.concat(columns, axis=1)
    # there is an option to load all abilities and also each of them separately - get rid of duplicates
    df = df.loc[:, ~df.columns.duplicated()]

    if "focus" in df.columns:
        df["focus"] = df["focus"].fillna(-1)
        df["focus"] = df["focus"].astype(int)

    df.loc[df["level"] > 20, "level"] = 21

    return df
