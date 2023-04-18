import json
from collections import defaultdict
from typing import Dict, List, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from training.analysis_functions import DataFrameType


_DEFAULT_TEST_SIZE: float = 0.25
"""Default value of fraction of the dataset to include in test split."""


def _get_book_names_from_dataframe(dataframe: DataFrameType) -> List[str]:
    """
    Collects unique values of "book" column in dataframe.\n
    :param dataframe: Processed dataframe.
    :return: List of books' names.
    """
    try:
        return dataframe.book.unique()
    except AttributeError as e:
        print(f"_get_book_names_from_dataframe: Error occurred: {e}.")
        return []


def _get_grouped_book_names(dataframe: pd.DataFrame) -> Dict[int, List[str]]:
    """
    Groups names of books present in "book" column in dataframe by the year the books were published.\n
    :param dataframe: Processed dataframe.
    :return: Dictionary containing list of books for each year.
    """
    with open("../training/book_year_mapping.json", "r") as mapping_file:
        book_year_mapping = json.loads("".join(mapping_file.readlines()))

    grouped_books_per_year = defaultdict(list)
    book_names = _get_book_names_from_dataframe(dataframe)
    for book_name in book_names:
        if book_year := book_year_mapping.get(book_name):
            grouped_books_per_year[book_year].append(book_name)
        else:
            grouped_books_per_year[0].append(book_name)
    return grouped_books_per_year


def _get_dataframe_with_oldest_books(
    dataframe: DataFrameType, test_size: float = _DEFAULT_TEST_SIZE
) -> DataFrameType:
    """
    Extracts from dataframe rows with the oldest books. Number of extracted rows is equal to
    a fraction of initial number of rows defined in test_size.\n
    :param dataframe: Processed dataframe.
    :param test_size: Fraction of the dataset to include in test split. It should be a float number between 0.0 and 1.0.
    :return: Dataframe containing extracted rows.
    """
    books_per_year = _get_grouped_book_names(dataframe)
    filtered_dataframe = pd.DataFrame(columns=dataframe.columns)
    remaining_rows_num = int((1 - test_size) * dataframe.shape[0])
    for year in sorted(books_per_year.keys()):
        for book_name in books_per_year[year]:
            book_df = dataframe.loc[dataframe["book"] == book_name]
            included_rows_num = min(remaining_rows_num, book_df.shape[0])
            filtered_dataframe = pd.concat(
                [filtered_dataframe, book_df[:included_rows_num]]
            )
            remaining_rows_num -= included_rows_num
            if remaining_rows_num == 0:
                return filtered_dataframe
    return filtered_dataframe


def _get_chronological_split_results(
    dataframe: DataFrameType,
) -> Tuple[DataFrameType, DataFrameType, DataFrameType, DataFrameType]:
    """
    Splits dataframe into training and testing sets chronologically.\n
    :param dataframe: Processed dataframe.
    :return: Two dataframes (first one for training and second one for testing) and two columns in the same order.
    """
    X_train = _get_dataframe_with_oldest_books(dataframe)
    if not X_train.empty:
        X_test = dataframe.drop(X_train.index)
        y_train = X_train.pop("level")
        y_test = X_test.pop("level")
        return X_train, X_test, y_train, y_test
    else:
        print(
            "_get_chronological_split_results: No books were found in dataframe. Dataframe will be split randomly."
        )
        return _get_random_split_results(dataframe)


def _get_random_split_results(
    dataframe: DataFrameType, test_size: float = _DEFAULT_TEST_SIZE
) -> Tuple[DataFrameType, DataFrameType, DataFrameType, DataFrameType]:
    """
    Splits dataframe into training and testing sets randomly.\n
    :param dataframe: Processed dataframe.
    :param test_size: Fraction of the dataset to include in test split. It should be a float number between 0.0 and 1.0.
    :return: Two dataframes (first one for training and second one for testing) and two columns in the same order.
    """
    X, y = dataframe.drop("level", axis="columns"), dataframe["level"]
    return train_test_split(X, y, test_size=test_size, random_state=0, shuffle=True)


def split_dataframe(
    dataframe: DataFrameType,
    test_size: float = _DEFAULT_TEST_SIZE,
    random_split: bool = False,
) -> Tuple[DataFrameType, DataFrameType, DataFrameType, DataFrameType]:
    """
    Splits dataframe to dataframes allowing training and testing of ML models. Requires "level" column to be
    present in initial dataframe.\n
    :param dataframe: Processed dataframe.
    :param test_size: Fraction of the dataset to include in test split. It should be a float number between 0.0 and 1.0.
    :param random_split: If False, splits dataframe chronologically so that training set contains rows with
    the oldest books from initial dataframe and testing set contains the newest. Otherwise, the dataframe is
    split randomly.
    :return: Two dataframes (first one for training and second one for testing) and two columns in the same order.
    """
    if not 0.0 < test_size < 1.0:
        raise ValueError("test_size must be between 0.0 and 1.0.")

    if "level" not in dataframe:
        raise ValueError('Dataframe must contain "level" column.')

    if random_split:
        return _get_random_split_results(dataframe)

    return _get_chronological_split_results(dataframe)
