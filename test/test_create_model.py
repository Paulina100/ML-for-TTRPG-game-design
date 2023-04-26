import random

import pandas as pd
import pytest
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV

from training.create_model import create_model, get_fitted_model


@pytest.fixture
def generated_train_set() -> tuple[pd.DataFrame, pd.Series]:
    n = 10
    data = {
        "cha": [random.randint(-5, 5) for _ in range(n)],
        "con": [random.randint(-5, 5) for _ in range(n)],
        "dex": [random.randint(-5, 5) for _ in range(n)],
    }

    X_train = pd.DataFrame(data=data)
    y_train = pd.Series(data=[random.randint(-1, 5) for _ in range(n)], name="lvl")

    return X_train, y_train


def test_create_linear_regression(generated_train_set):
    X_train, y_train = generated_train_set

    model = get_fitted_model("train_linear_regression", X_train, y_train)

    assert type(model) == RidgeCV


def test_create_random_forest(generated_train_set):
    X_train, y_train = generated_train_set
    model = get_fitted_model("train_random_forest", X_train, y_train)

    assert type(model.best_estimator_) == RandomForestRegressor


def test_wrong_classifier_name():
    with pytest.raises(ValueError):
        model = create_model("train_wrong_classifier_name")
