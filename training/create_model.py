import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import RandomizedSearchCV

from training.constants import RANDOM_STATE


def get_fitted_model(
    classifier_name: str,
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> RidgeCV | RandomizedSearchCV:
    """
    Creates chosen model, performs tuning and fits\n
    :param X_train: train set with features to use during fitting
    :param y_train: train set with values to predict
    :param classifier_name: name of a chosen classifier:
            train_linear_regression or train_random_forest
    :return: trained classifier of a chosen type
    """
    model = fit_model(X_train, y_train, create_model(classifier_name))

    return model


def create_model(
    classifier_name: str,
):
    """
    Creates chosen model\n
    :param classifier_name: name of a chosen classifier:
            train_linear_regression or train_random_forest
    :return: chosen classifier
    """
    match classifier_name:
        case "train_linear_regression":
            model = RidgeCV(alphas=np.linspace(1e-3, 1, 10000))
        case "train_random_forest":
            rf = RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1)
            hyper_params = {
                "n_estimators": [x for x in range(200, 2001, 200)],
                "max_features": [0.1, 0.2, 0.3, 0.4, 0.5],
                "max_depth": np.concatenate(
                    ([int(x) for x in np.linspace(10, 110, num=11)], [None])
                ),
            }
            model = RandomizedSearchCV(
                estimator=rf,
                param_distributions=hyper_params,
                n_iter=100,
                scoring="neg_mean_absolute_error",
                cv=3,
                verbose=2,
                random_state=RANDOM_STATE,
                return_train_score=True,
            )
        case _:
            raise ValueError(f"Classifier {classifier_name} is unsupported")

    return model


def fit_model(
    X_train: pd.DataFrame, y_train: pd.Series, model: RidgeCV | RandomizedSearchCV
) -> RidgeCV | RandomizedSearchCV:
    """
    Performs fitting using given model and train data\n
    :param X_train: train set with features to use during fitting
    :param y_train: train set with values to predict
    :param model: model to fit
    :return: trained model
    """
    if "book" in X_train.columns:
        raise ValueError("You have to drop column 'book' first")

    model.fit(X_train, y_train)

    return model
