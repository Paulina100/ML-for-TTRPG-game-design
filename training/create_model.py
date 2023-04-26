from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV
import pandas.core.frame
import pandas.core.series
from sklearn.model_selection import RandomizedSearchCV
import numpy as np


def create_model(
    classifier_name: str,
    X_train: pandas.core.frame.DataFrame,
    y_train: pandas.core.series.Series,
):
    """
    Creates chosen model, performs tuning and fit
    :param X_train: train set with features to use during fitting
    :param y_train: train set with values to predict
    :param classifier_name: name of a chosen classifier:
            train_linear_regression or train_random_forest
    :return: trained classifier of a chosen type
    """
    if "book" in X_train.columns:
        print("You have to drop column 'book' first")
        # drop_source_column(X_train)
        return None

    match classifier_name:
        case "train_linear_regression":
            model = RidgeCV(alphas=np.linspace(1e-3, 1, 10000))
        case "train_random_forest":
            rf = RandomForestRegressor(random_state=0, n_jobs=-1)
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
                random_state=42,
                return_train_score=True,
            )
        case _:
            return None

    model.fit(X_train, y_train)

    return model
