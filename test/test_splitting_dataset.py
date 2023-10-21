from test.constants import DATASET_PATHS

import pytest

from training.creating_dataset import load_and_preprocess_data
from training.splitting_dataset import (
    get_chronological_split_results,
    get_dataframe_with_oldest_books,
    get_date_books_mapping,
    get_random_split_results,
    split_dataframe,
)


# get_grouped_book_names
def test_get_date_books_mapping():
    grouped_books = get_date_books_mapping()
    assert grouped_books.shape == (49, 2)


# get_dataframe_with_oldest_books
def test_get_dataframe_with_oldest_books():
    test_size = 0.5
    df = load_and_preprocess_data(
        DATASET_PATHS,
        characteristics=[
            "cha",
            "con",
            "dex",
            "int",
            "str",
            "wis",
            "ac",
            "hp",
            "focus",
            "fortitude",
        ],
    )
    oldest_books_df = get_dataframe_with_oldest_books(df, test_size)
    assert oldest_books_df.shape[0] >= int((1 - test_size) * df.shape[0])

    books = sorted(oldest_books_df.book.unique())
    expected_books = sorted(
        ["Pathfinder Bestiary", "Pathfinder Core Rulebook", "Pathfinder Bestiary 2"]
    )
    assert books == expected_books


# get_chronological_split_results
def test_get_chronological_split_results():
    test_size = 0.5
    df = load_and_preprocess_data(
        DATASET_PATHS,
        characteristics=[
            "cha",
            "con",
            "dex",
            "int",
            "str",
            "wis",
            "ac",
            "hp",
            "focus",
            "fortitude",
        ],
    )
    X_train, X_test, y_train, y_test = get_chronological_split_results(df, test_size)
    assert "level" not in X_train
    assert "level" not in X_test
    assert X_train.shape[0] + X_test.shape[0] == df.shape[0]
    assert y_train.shape[0] + y_test.shape[0] == df.shape[0]

    df = df.drop(columns="book")
    with pytest.raises(ValueError):
        X_train, X_test, y_train, y_test = get_chronological_split_results(
            df, test_size
        )


# _get_random_split_results
def test_get_random_split_results():
    test_size = 0.5
    df = load_and_preprocess_data(
        DATASET_PATHS,
        characteristics=[
            "cha",
            "con",
            "dex",
            "int",
            "str",
            "wis",
            "ac",
            "hp",
            "focus",
            "fortitude",
        ],
    )
    X_train, X_test, y_train, y_test = get_random_split_results(df, test_size)
    assert "level" not in X_train
    assert "level" not in X_test
    assert X_train.shape[0] + X_test.shape[0] == df.shape[0]
    assert y_train.shape[0] + y_test.shape[0] == df.shape[0]


# split_dataframe
def test_split_dataframe():
    test_size = 1.5
    df = load_and_preprocess_data(
        DATASET_PATHS,
        characteristics=[
            "cha",
            "con",
            "dex",
            "int",
            "str",
            "wis",
            "ac",
            "hp",
            "focus",
            "fortitude",
        ],
    )
    with pytest.raises(ValueError):
        X_train, X_test, y_train, y_test = split_dataframe(df, test_size)

    test_size = 0.5
    df = df.drop(columns="level")
    with pytest.raises(ValueError):
        X_train, X_test, y_train, y_test = split_dataframe(df, test_size)
