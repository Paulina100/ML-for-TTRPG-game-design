import pytest

from training.creating_dataset import create_dataframe
from training.splitting_dataset import (
    _get_book_names_from_dataframe,
    _get_grouped_book_names,
    _get_dataframe_with_oldest_books,
    _get_chronological_split_results,
    _get_random_split_results,
    split_dataframe,
)


# _get_book_names_from_dataframe
def test_get_book_names_from_dataframe():
    df = create_dataframe()
    books = sorted(_get_book_names_from_dataframe(df))
    expected_books = sorted(
        [
            "Pathfinder Bestiary",
            "Pathfinder Bestiary 2",
            "Pathfinder Bestiary 3",
            "Pathfinder Core Rulebook",
        ]
    )
    assert books == expected_books

    df = df.drop(columns="book")
    books = _get_book_names_from_dataframe(df)
    assert len(books) == 0


# _get_grouped_book_names
def test_get_grouped_book_names():
    df = create_dataframe()
    grouped_books = _get_grouped_book_names(df)
    expected_grouped_books = {
        2019: ["Pathfinder Bestiary", "Pathfinder Core Rulebook"],
        2020: ["Pathfinder Bestiary 2"],
        2021: ["Pathfinder Bestiary 3"],
    }
    assert grouped_books == expected_grouped_books

    df.at[0, "book"] = "Not Existing Book"
    grouped_books = _get_grouped_book_names(df)
    expected_grouped_books[0] = ["Not Existing Book"]
    assert grouped_books == expected_grouped_books

    df = df.drop(columns="book")
    grouped_books = _get_grouped_book_names(df)
    assert len(grouped_books) == 0


# _get_dataframe_with_oldest_books
def test_get_dataframe_with_oldest_books():
    test_size = 0.5
    df = create_dataframe()
    oldest_books_df = _get_dataframe_with_oldest_books(df, test_size)
    assert oldest_books_df.shape[0] == int((1 - test_size) * df.shape[0])

    books = sorted(oldest_books_df.book.unique())
    expected_books = sorted(
        ["Pathfinder Bestiary", "Pathfinder Core Rulebook", "Pathfinder Bestiary 2"]
    )
    assert books == expected_books


# _get_chronological_split_results
def test_get_chronological_split_results():
    test_size = 0.5
    df = create_dataframe()
    X_train, X_test, y_train, y_test = _get_chronological_split_results(df, test_size)
    assert "level" not in X_train
    assert "level" not in X_test
    assert X_train.shape[0] + X_test.shape[0] == df.shape[0]
    assert y_train.shape[0] + y_test.shape[0] == df.shape[0]

    df = df.drop(columns="book")
    X_train, X_test, y_train, y_test = _get_chronological_split_results(df, test_size)
    assert "level" not in X_train
    assert "level" not in X_test
    assert X_train.shape[0] + X_test.shape[0] == df.shape[0]
    assert y_train.shape[0] + y_test.shape[0] == df.shape[0]


# _get_random_split_results
def test_get_random_split_results():
    test_size = 0.5
    df = create_dataframe()
    X_train, X_test, y_train, y_test = _get_random_split_results(df, test_size)
    assert "level" not in X_train
    assert "level" not in X_test
    assert X_train.shape[0] + X_test.shape[0] == df.shape[0]
    assert y_train.shape[0] + y_test.shape[0] == df.shape[0]


# split_dataframe
def test_split_dataframe():
    test_size = 1.5
    df = create_dataframe()
    with pytest.raises(ValueError):
        X_train, X_test, y_train, y_test = split_dataframe(df, test_size)

    test_size = 0.5
    df = df.drop(columns="level")
    with pytest.raises(ValueError):
        X_train, X_test, y_train, y_test = split_dataframe(df, test_size)
