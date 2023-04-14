import os.path
from copy import deepcopy

import pandas as pd
import numpy as np
import pandas.core.frame
import pandas.core.series

from notebooks.data_analysis.analysis_functions import (
    import_merged_bestiaries,
    unpack_column,
)


def create_dataframe(
    books: list[str] = [
        "pathfinder_2e_data/pathfinder-bestiary.db",
        "pathfinder_2e_data/pathfinder-bestiary-2.db",
        "pathfinder_2e_data/pathfinder-bestiary-3.db",
    ],
    characteristics: list[str] = [
        "system/abilities",
        "system/attributes/ac",
        "system/attributes/hp",
    ],
) -> pandas.core.frame.DataFrame:
    loading_methods = {"system/abilities": move_values_level_up(value_name="mod")}
    check_paths(books)
    bestiary = import_merged_bestiaries(books)
    bestiary = bestiary[bestiary[type] == "npc"]
    df = pd.DataFrame()

    for characteristic in characteristics:
        if characteristic in loading_methods.keys():
            df = pd.concat(
                [
                    df,
                    loading_methods.get(characteristic)(
                        df=get_sub_column(characteristic)
                    ),
                ]
            )


def check_paths(paths: list[str]) -> None:
    """
    Throws exception if file does not exist or has a wrong extension
    :param paths: list of paths to books to load
    :return:
    """
    for path in paths:
        if not os.path.isfile(path):
            raise Exception(f"Path {path} does not exist")
        if path.endswith(".db") or path.endswith(".json"):
            raise Exception(f"Expected db or json file\n {path}")


def move_values_level_up(
    df: pandas.core.frame.DataFrame, value_name: str
) -> pandas.core.frame.DataFrame:
    return df.applymap(lambda x: x.get(value_name), na_action="ignore")


def get_sub_column(
    book: pandas.core.frame.DataFrame, sub_column_path: str
) -> pandas.core.frame.DataFrame:
    sub_col = deepcopy(book)
    for col in sub_column_path.split("/"):
        sub_col = unpack_column(sub_col, col)

    return sub_col
