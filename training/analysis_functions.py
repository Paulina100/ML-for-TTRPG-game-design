from typing import List, Optional, NewType

import pandas as pd
import numpy as np
import pandas.core.frame
import pandas.core.series

DataFrameType = NewType("DataFrameType", pandas.core.frame.DataFrame)


def get_merged_bestiaries(paths_to_bestiaries: List[str]) -> DataFrameType:
    """
    Returns merged books

    :param paths_to_bestiaries: list of paths to books
    :return: DataFrame with data from files which paths were given
    """
    result = [pd.read_json(book, lines=True) for book in paths_to_bestiaries]
    return pd.concat(result, join="outer", axis=0).fillna(np.nan).reset_index(drop=True)


def unpack_column(
    df: DataFrameType, column_name: str, print_info: bool = False
) -> Optional[DataFrameType]:
    """
    Unpacks dict and changes it to DataFrame

    :param df: DataFrame with column with dict
    :param column_name: name of the colum with dict - column should contain dictionary
    :param print_info: print or not: first row and Len of that row
    :return: DataFrame with values from chosen column
    """
    new_df = df[column_name].apply(pd.Series)
    if print_info:
        print("unpack_column: First row:")
        print(new_df.iloc[0])
        print(f"Len = {len(new_df.iloc[0])}")
    return new_df
