import json
import os.path

import numpy as np
import pandas as pd


OTHER_SPEEDS = [
    "fly",
    "swim",
    "climb",
]
OTHER_SPEED_PATH = "system.attributes.speed.otherSpeeds"

RESISTANCES = [
    "fire_resistance",
    "cold_resistance",
    "electricity_resistance",
    "acid_resistance",
    "piercing_resistance",
    "slashing_resistance",
    "physical_resistance",
    "bludgeoning_resistance",
    "mental_resistance",
    "poison_resistance",
    "all-damage_resistance",
]
RESISTANCE_PATH = "system.attributes.resistances"

WEAKNESSES = [
    "cold-iron_weakness",
    "good_weakness",
    "fire_weakness",
    "cold_weakness",
    "area-damage_weakness",
    "splash-damage_weakness",
    "evil_weakness",
    "slashing_weakness",
]
WEAKNESSES_PATH = "system.attributes.weaknesses"


CHARACTERISTICS_COLUMNS = {
    "con": "system.abilities.con.mod",
    "dex": "system.abilities.dex.mod",
    "cha": "system.abilities.cha.mod",
    "int": "system.abilities.int.mod",
    "str": "system.abilities.str.mod",
    "wis": "system.abilities.wis.mod",
    "ac": "system.attributes.ac.value",
    "hp": "system.attributes.hp.value",
    "perception": "system.attributes.perception.value",
    "fortitude": "system.saves.fortitude.value",
    "reflex": "system.saves.reflex.value",
    "will": "system.saves.will.value",
    "focus": "system.resources.focus.value",
    "level": "system.details.level.value",
    "book": "system.details.source.value",
    "land_speed": "system.attributes.speed.value",
    "immunities": "system.attributes.immunities",
    "fly": "fly",
    "swim": "swim",
    "climb": "climb",
    "fire_resistance": "fire_resistance",
    "cold_resistance": "cold_resistance",
    "electricity_resistance": "electricity_resistance",
    "acid_resistance": "acid_resistance",
    "piercing_resistance": "piercing_resistance",
    "slashing_resistance": "slashing_resistance",
    "physical_resistance": "physical_resistance",
    "bludgeoning_resistance": "bludgeoning_resistance",
    "mental_resistance": "mental_resistance",
    "poison_resistance": "poison_resistance",
    "all-damage_resistance": "all-damage_resistance",
    "cold-iron_weakness": "cold-iron_weakness",
    "good_weakness": "good_weakness",
    "fire_weakness": "fire_weakness",
    "cold_weakness": "cold_weakness",
    "area-damage_weakness": "area-damage_weakness",
    "splash-damage_weakness": "splash-damage_weakness",
    "evil_weakness": "evil_weakness",
    "slashing_weakness": "slashing_weakness",
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

    if not (path.endswith(".db") or path.endswith(".json")):
        raise ValueError(f"Expected db or json file, got {path}")

    return True


def get_characteristic_from_list(cell_value, characteristic_type):
    if not cell_value or np.all(pd.isnull(cell_value)):
        return 0
    # print(cell_value)
    res = [x.get("value") for x in cell_value if x.get("type") == characteristic_type]
    return 0 if len(res) == 0 else res[0]


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
    bestiary = bestiary.filter(regex="system", axis="columns")

    for resistance in [r for r in characteristics if r in RESISTANCES]:
        bestiary[resistance] = bestiary[RESISTANCE_PATH].apply(
            lambda x: get_characteristic_from_list(
                cell_value=x, characteristic_type=resistance
            )
        )

    for weakness in [w for w in characteristics if w in WEAKNESSES]:
        bestiary[weakness] = bestiary[WEAKNESSES_PATH].apply(
            lambda x: get_characteristic_from_list(
                cell_value=x, characteristic_type=weakness.replace("_weakness", "")
            )
        )

    if "immunities" in characteristics:
        immunities_path = CHARACTERISTICS_COLUMNS.get("immunities")
        bestiary[immunities_path] = bestiary[immunities_path].apply(
            lambda x: 0 if np.all(pd.isnull(x)) else len(x)
        )

    for speed in [s for s in characteristics if s in OTHER_SPEEDS]:
        # fly_path = CHARACTERISTICS_COLUMNS.get("fly")
        bestiary[speed] = bestiary[OTHER_SPEED_PATH].apply(
            lambda x: get_characteristic_from_list(x, speed)
        )

    COLS_TO_EXTRACT = pd.DataFrame(
        data=[
            (characteristic, CHARACTERISTICS_COLUMNS.get(characteristic))
            for characteristic in characteristics + ["book", "level"]
        ],
        columns=["target_name", "raw_name"],
    )

    raw_names = COLS_TO_EXTRACT["raw_name"]
    target_names = COLS_TO_EXTRACT["target_name"]

    # to not have Series names as a part of final df
    target_names.name = None

    df = bestiary[raw_names]
    df.columns = target_names

    if "focus" in df.columns:
        # silent warning (SettingWithCopyWarning) about view and copy
        # we don't need to go back to the original df - no matter if it is a view
        with pd.option_context("mode.chained_assignment", None):
            df["focus"] = df["focus"].fillna(0)
            df["focus"] = df["focus"].astype(int)

    if "land_speed":
        with pd.option_context("mode.chained_assignment", None):
            df["land_speed"] = df["land_speed"].fillna(0)

    df.loc[df["level"] > 20, "level"] = 21

    return df
