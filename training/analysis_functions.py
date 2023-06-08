import warnings
from copy import deepcopy

import numpy as np
import pandas as pd


def get_merged_bestiaries(paths_to_bestiaries: list[str]) -> pd.DataFrame:
    """
    Returns merged books

    :param paths_to_bestiaries: list of paths to books
    :return: DataFrame with data from files which paths were given
    """
    result = [pd.read_json(book, lines=True) for book in paths_to_bestiaries]
    return pd.concat(result, join="outer", axis=0).fillna(np.nan).reset_index(drop=True)


def unpack_column(
    df: pd.DataFrame, column_name: str, print_info: bool = False
) -> pd.DataFrame:
    """
    Unpacks dict and changes it to DataFrame

    :param df: DataFrame with column with dict
    :param column_name: name of the colum with dict - column should contain dictionary
    :param print_info: print or not: first row and Len of that row
    :return: DataFrame with values from chosen column
    """
    with warnings.catch_warnings():
        # ignore future warning - warning about deprecated features
        # FutureWarning: The default dtype for empty Series will be 'object'
        # Project have fixed pandas version
        warnings.simplefilter(action="ignore", category=FutureWarning)
        new_df = df[column_name].apply(pd.Series)

    if print_info:
        print("unpack_column: First row:")
        print(new_df.iloc[0])
        print(f"Len = {len(new_df.iloc[0])}")
    return new_df


def _create_null_dataframe(index: list[int], columns: list[str]) -> pd.DataFrame:
    """
    Creates a dataframe which contains only null values

    :param index: List of indices to use for resulting frame
    :param columns: Column labels to use for resulting frame
    :return: DataFrame with given labels and columns and null data
    """
    return pd.DataFrame(index=index, columns=columns)


def unpack_column_with_null(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Unpacks chosen dictionary column even if there are rows with null value in that column and changes it to DataFrame.

    >>> df = pd.DataFrame({'col1':[{"s": "s", "x": 1}, np.nan], 'col2':[3, 4]})
    >>> df
            col1              col2
    0   {"s": "s", "x": 1}     3
    1        NaN               4

    If we want to unpack col1 function will use *unpack_column* to deal with non-null rows (like 0 here)
    and for null rows it will fill every subcolumn from col1 with nulls (like 1 here)

    >>> unpack_column_with_null(df, "col1")
         s      x
    0    s      1
    1   NaN    NaN

    :param df: DataFrame with column with dict
    :param column_name: name of the colum with dict - column should contain dictionary
    :return: DataFrame with values from chosen column, nulls in a row if there was no data in that row

    """
    notnull_df = unpack_column(df[df[column_name].notnull()], column_name)
    return pd.concat(
        [
            notnull_df,
            _create_null_dataframe(
                list(df[df[column_name].isnull()].index.values), notnull_df.columns
            ),
        ]
    ).sort_index()


def get_subcolumn(book: pd.DataFrame, subcolumn_path: str) -> pd.DataFrame:
    """
    Gets subcolumn of given DataFrame according to given path
    Gets subcolumn of given DataFrame according to given path or one level up column in the path if it is known that the next colum have missing data
    :param book: DataFrame with all data from book(s)
    :param subcolumn_path: path to subcolumn
    :return: chosen subcolumn as DataFrame
    """
    subcol = deepcopy(book)
    for col in subcolumn_path.split("/"):
        subcol = pd.DataFrame(data=unpack_column_with_null(subcol, col))

    return subcol
