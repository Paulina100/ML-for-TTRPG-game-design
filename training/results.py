import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, mean_squared_error


def print_check_predictions(y, y_pred):
    print(f"MSE: {mean_squared_error(y, y_pred):.2f}")
    print(f"RMSE: {mean_squared_error(y, y_pred, squared=False):.2f}\n")


def round_predictions(threshold: str | float, predict):
    """

    :param threshold:
    :param predict:
    :return:
    """
    if type(threshold) == str:
        if threshold != "round":
            raise ValueError(f"No round type named {threshold}")
        threshold_predict = np.round(predict).astype("int")
    else:
        if threshold > 1 or threshold < 0:
            raise ValueError(f"Incorrect threshold value: {threshold}")
        threshold_predict = np.where(
            (predict % 1) > threshold, np.ceil(predict), np.floor(predict)
        ).astype("int")

    return np.where(threshold_predict > 20, 21, threshold_predict)


def check_round_predictions(round_types: list[str | float], y, predict):
    """

    :param round_types:
    :param y:
    :param y_pred:
    :return:
    """
    print("Normal:")
    print_check_predictions(y, predict)

    for threshold in round_types:
        threshold_predict = round_predictions(threshold, predict)

        print(f"Round type: {threshold}")
        print_check_predictions(y, threshold_predict)


def plot_confusion_matrix(threshold, predict, y):
    round_predict = round_predictions(threshold, predict)
    cm = confusion_matrix(y, round_predict)

    # min possible level: -1, max possible level: 21
    labels = [i for i in range(-1, 22)]

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

    disp.plot()
    plt.title("Confusion matrix")
    plt.show()


def assess_regression_model(model, X_train, X_test, y_train, y_test, r2=False):
    # predict for train and test
    y_pred_test = model.predict(X_test)
    y_pred_train = model.predict(X_train)

    # calculate train and test RMSE
    rmse_train = mean_squared_error(y_train, y_pred_train, squared=False)
    rmse_test = mean_squared_error(y_test, y_pred_test, squared=False)
    mse_test = mean_squared_error(y_test, y_pred_test)

    if r2:
        # calculate R2
        r2 = model.score(X_train, y_train)
        print(f"R2: {r2:.2f}")

    # print train and test RMSE
    print(f"RMSE train: {rmse_train:.2f}")
    print(f"RMSE test: {rmse_test:.2f}")
    print(f"MSE test: {mse_test:.2f}\n")

    return rmse_test, mse_test
