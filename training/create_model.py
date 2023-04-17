from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LassoCV
import pandas.core.frame
import pandas.core.series
from sklearn.model_selection import GridSearchCV

CLASSIFIERS = {
    "train_linear_regression": LassoCV(n_alphas=1000, random_state=0),
    "train_random_forest": RandomForestClassifier(
        random_state=0, n_jobs=-1
    ),  # czy jakiś inny? RandomForestRegressor?
}


def create_model(
    classifier_name: str,
    X_train: pandas.core.frame.DataFrame,
    y_train: pandas.core.series.Series,
):
    """
    Creates chosen model, makes tuning and fits it
    :param y_train: dataframe with
    :param X_train:
    :param classifier_name: name of a chosen classifier
    :return: trained classifier of a chosen type
    """
    clf = create_clf_with_tuning(classifier_name)

    if clf is None:
        return

    # palce for tuning

    clf.fit(X_train, y_train)

    return clf


def create_clf_with_tuning(classifier_name: str):
    """
    tuning the hyper-parameters of an estimator
    :param clf: classifier
    :param classifier_name: name of classifier
    :return: classifier after tuning
    """
    base_clf = CLASSIFIERS.get(classifier_name)
    if classifier_name == "train_linear_regression" or base_clf is None:
        return base_clf

    hyper_params = {
        "n_estimators": [100, 200, 300, 400, 500],
        "max_features": ["sqrt", "log2", 0.1, 0.2, 0.3, 0.4, 0.5, None],
        "max_depth": [3, 6, 9],
        "max_leaf_nodes": [3, 6, 9],
    }
    clf = GridSearchCV(
        estimator=base_clf,
        param_grid=hyper_params,
        verbose=2,
        return_train_score=True,
    )

    return clf
