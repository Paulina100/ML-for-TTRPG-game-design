from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LassoCV
import pandas.core.frame
import pandas.core.series


CLASSIFIERS = {
    "train_linear_regression": LassoCV(n_alphas=1000, random_state=0),
    "train_random_forest": RandomForestClassifier(random_state=0, n_jobs=-1),
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
    clf = CLASSIFIERS.get(classifier_name)

    if clf is None:
        return

    # palce for tuning

    clf.fit(X_train, y_train)

    return clf


def _tuning(clf, classifier_name: str):
    """
    tuning the hyper-parameters of an estimator
    :param clf: classifier
    :param classifier_name: name of classifier
    :return: classifier after tuning
    """
    if classifier_name == "train_linear_regression":
        return clf

    # other cases
    # gridsearch??
    return clf
