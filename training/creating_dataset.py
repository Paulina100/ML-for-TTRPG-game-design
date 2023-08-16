import json
import os.path

import numpy as np
import pandas as pd


OTHER_SPEEDS = {
    "fly",
    "swim",
    "climb",
}
OTHER_SPEED_PATH = "system.attributes.speed.otherSpeeds"

RESISTANCES = {
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
}
RESISTANCE_PATH = "system.attributes.resistances"

WEAKNESSES = {
    "cold-iron_weakness",
    "good_weakness",
    "fire_weakness",
    "cold_weakness",
    "area-damage_weakness",
    "splash-damage_weakness",
    "evil_weakness",
    "slashing_weakness",
}
WEAKNESSES_PATH = "system.attributes.weaknesses"

SPECIAL_CHARACTERISTICS = {
    "melee",
    "ranged",
    "spells",
}


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


def split_characteristics_into_groups(characteristics):
    speeds = OTHER_SPEEDS.intersection(characteristics)
    weaknesses = WEAKNESSES.intersection(characteristics)
    resistances = RESISTANCES.intersection(characteristics)
    special_characteristics = SPECIAL_CHARACTERISTICS.intersection(characteristics)
    characteristics_rename = [
        ch for ch in characteristics if ch in CHARACTERISTICS_COLUMNS.keys()
    ]

    return (
        speeds,
        weaknesses,
        resistances,
        special_characteristics,
        characteristics_rename,
    )


def get_characteristic_from_list(cell_value, characteristic_type):
    if not cell_value or np.all(pd.isnull(cell_value)):
        return 0

    res = [x.get("value") for x in cell_value if x.get("type") == characteristic_type]
    return 0 if len(res) == 0 else res[0]


def get_nr_of_spells_with_lvl(items_list, lvl):
    spells = [
        i
        for i in items_list
        if i.get("type") == "spell"
        and i.get("system").get("category").get("value") == "spell"
    ]

    spells = [
        i for i in spells if "cantrip" not in i.get("system").get("traits").get("value")
    ]

    return len([s for s in spells if s.get("system").get("level").get("value") == lvl])


def count_damage(damage_dict):
    total_expected_val = 0

    for key, value in damage_dict.items():
        damage = value.get("damage")

        if not "d" in damage:
            return int(damage)
        roll_nr, dice_type = damage.split("d")
        add = 0
        if "+" in dice_type:
            dice_type, add = dice_type.split("+")
            add = int(add)
        if "-" in dice_type:
            dice_type, add = dice_type.split("-")
            add = -int(add)
        roll_nr, dice_type = int(roll_nr), int(dice_type)
        total_expected_val += (
            roll_nr * sum([i for i in range(1, dice_type + 1)]) / dice_type
        ) + add

    return total_expected_val


def get_max_melee_bonus_damage(items_list, weaponType):
    melee = [
        i.get("system")
        for i in items_list
        if i.get("type") == "melee"
        and i.get("system").get("weaponType").get("value") == weaponType
    ]
    if len(melee) == 0:
        return 0, 0
    max_bonus_indx, max_bonus = max(
        [(i, melee[i].get("bonus").get("value")) for i in range(len(melee))],
        key=lambda x: x[1],
    )

    return max_bonus, count_damage(melee[max_bonus_indx].get("damageRolls"))


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
    # bestiary = bestiary.filter(regex="system", axis="columns")

    (
        speeds,
        weaknesses,
        resistances,
        special_characteristics,
        characteristics,
    ) = split_characteristics_into_groups(characteristics)
    print(speeds, weaknesses, resistances, special_characteristics, characteristics)

    if "immunities" in characteristics:
        with pd.option_context("mode.chained_assignment", None):
            immunities_path = CHARACTERISTICS_COLUMNS.get("immunities")
            bestiary[immunities_path] = bestiary[immunities_path].apply(
                lambda x: 0 if np.all(pd.isnull(x)) else len(x)
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

    for resistance in resistances:
        with pd.option_context("mode.chained_assignment", None):
            # silent warning (SettingWithCopyWarning) about view and copy
            # we don't need to go back to the original df - no matter if it is a view
            df[resistance] = bestiary[RESISTANCE_PATH].apply(
                lambda x: get_characteristic_from_list(
                    cell_value=x, characteristic_type=resistance
                )
            )

    for weakness in weaknesses:
        with pd.option_context("mode.chained_assignment", None):
            df[weakness] = bestiary[WEAKNESSES_PATH].apply(
                lambda x: get_characteristic_from_list(
                    cell_value=x, characteristic_type=weakness.replace("_weakness", "")
                )
            )

    for speed in speeds:
        # fly_path = CHARACTERISTICS_COLUMNS.get("fly")
        with pd.option_context("mode.chained_assignment", None):
            df[speed] = bestiary[OTHER_SPEED_PATH].apply(
                lambda x: get_characteristic_from_list(x, speed)
            )

    if "spells" in special_characteristics:
        MAX_SPELL_LVL = 9
        with pd.option_context("mode.chained_assignment", None):
            for i in range(1, MAX_SPELL_LVL + 1):
                df[f"spells_nr_lvl_{i}"] = bestiary["items"].apply(
                    lambda X: get_nr_of_spells_with_lvl(X, i)
                )

    if "melee" in special_characteristics:
        with pd.option_context("mode.chained_assignment", None):
            df["melee_max_bonus"], df["melee_damage_exp_val"] = zip(
                *bestiary["items"].apply(
                    lambda x: get_max_melee_bonus_damage(x, "melee")
                )
            )

    if "melee" in special_characteristics:
        with pd.option_context("mode.chained_assignment", None):
            df["ranged_max_bonus"], df["ranged_damage_exp_val"] = zip(
                *bestiary["items"].apply(
                    lambda x: get_max_melee_bonus_damage(x, "ranged")
                )
            )

    if "focus" in df.columns:
        with pd.option_context("mode.chained_assignment", None):
            df["focus"] = df["focus"].fillna(0)
            df["focus"] = df["focus"].astype(int)

    if "land_speed" in df.columns:
        with pd.option_context("mode.chained_assignment", None):
            df["land_speed"] = df["land_speed"].fillna(0)

    df.loc[df["level"] > 20, "level"] = 21

    return df
