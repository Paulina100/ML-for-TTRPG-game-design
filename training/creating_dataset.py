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
    "con": "system.abilities.con.mod",
    "mod": "system.abilities.dex.mod",
    "cha": "system.abilities.cha.mod",
    "int": "system.abilities.int.mod",
    "str": "system.abilities.str.mod",
    "wis": "system.abilities.wis.mod",
    # "abilities": "abilities" # end
    "ac": "system.attributes.ac.value",
    "hp": "system.attributes.hp.value",
    "perception": "system.attributes.perception.value",
    # "saves": "saves"
    "fortitude": "system.saves.fortitude.value",
    "reflex": "system.saves.reflex.value",
    "will": "system.saves.will.value",
    # "saves": "saves" #end
    "focus": "system.resources.focus.value",
    "level": "system.details.level.value",
    "book": "system.details.source.value",
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
    paths_to_books: list[str],
    characteristics: list[str],
) -> pd.DataFrame:
    """
    Creates dataframe containing chosen characteristics, level and source book of monsters from chosen books

    :param paths_to_books: list of paths of books to load
    :param characteristics: list of characteristics to load
    :return: DataFrame with monsters (NPC) from chosen books and with chosen characteristics and their origin book
    """
    data = []

    for path in paths_to_books:
        is_path_correct(path)
        with open(path) as file:
            # loading json strings from files
            data += [json.loads(line) for line in file]
            file.close()

    bestiary = pd.json_normalize(data)
    # only npc monsters
    bestiary = bestiary[bestiary["type"] == "npc"]
    # only system column (all characteristics are there)
    bestiary = bestiary.filter(regex="system", axis=1)

    columns = []
    for characteristic in characteristics + ["book", "level"]:
        # different way of loading data: abilities and saves is a group of characteristics
        if characteristic in ["abilities", "saves"]:
            subcolumns = bestiary.filter(regex=characteristic, axis=1)

            # in case of saves we have to filter to extract only useful columns
            if characteristic == "saves":
                subcolumns = subcolumns.filter(regex="value", axis=1)

            # renaming columns to simpler names of characteristics- group of characteristics=>df rename group of columns
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
