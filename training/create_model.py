import lightgbm as lightgbm
import numpy as np
import optuna.integration.lightgbm as opt_lgb
import pandas as pd
from lightgbm import early_stopping, log_evaluation
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold, RandomizedSearchCV

from training.constants import RANDOM_STATE


def get_fitted_model(
    classifier_name: str,
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> RidgeCV | RandomizedSearchCV | lightgbm.Booster:
    """
    Creates chosen model, performs tuning and fits\n
    :param X_train: train set with features to use during fitting
    :param y_train: train set with values to predict
    :param classifier_name: name of a chosen classifier:
            linear_regression or random_forest
    :return: trained classifier of a chosen type
    """
    if classifier_name == "lightgbm":
        return lightgbm_fit(X_train, y_train)

    model = create_model(classifier_name)
    model.fit(X_train, y_train)

    return model


def create_model(classifier_name: str):
    """
    Creates chosen model\n
    :param classifier_name: name of a chosen classifier:
            linear_regression or random_forest
    :return: chosen classifier
    """
    match classifier_name:
        case "linear_regression":
            model = RidgeCV(alphas=np.linspace(1e-3, 1, 10000))
        case "random_forest":
            rf = RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1)
            hyper_params = {
                "n_estimators": [
                    int(x) for x in np.linspace(start=100, stop=800, num=8)
                ],
                "max_features": [0.1, 0.2, 0.3, 0.4, 0.5],
                "max_depth": list(range(10, 111, 10)) + [None],
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


def lightgbm_fit(X_train, y_train) -> lightgbm.Booster:
    """
    Performs tuning and fits lightgbm model\n
    :param X_train: train set with features to use during fitting
    :param y_train: train set with values to predict
    :return: trained lightgbm
    """
    lgb_train = opt_lgb.Dataset(X_train, y_train)
    params = {
        "boosting_type": "gbdt",
        "objective": "regression",
        "metric": "l2",
        "verbosity": -1,
    }
    tuner = opt_lgb.LightGBMTunerCV(
        params,
        lgb_train,
        folds=KFold(n_splits=5),
        num_boost_round=10000,
        callbacks=[early_stopping(100), log_evaluation(100)],
    )
    tuner.run()
    best_params = tuner.best_params

    lgb_tuned = lightgbm.train(
        best_params,
        lgb_train,
        num_boost_round=10000,
    )
    return lgb_tuned
