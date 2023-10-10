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


def plot_summary(results, measure_type, figsize=(20, 8)):
    bar_width = 0.25
    fig, ax = plt.subplots(1, figsize=figsize)
    ax.grid()
    fig.autofmt_xdate()
    plt.grid(axis="y", linestyle="--")

    labels = results.apply(
        lambda row: row["Tuning type"] + " " + str(row["Number of characteristics"]),
        axis="columns",
    )
    labels = dict.fromkeys(labels).keys()
    chronological = []
    random = []

    for i, l in enumerate(labels):
        t, nr = l.split(" ")
        temp = results[
            (results["Tuning type"] == t)
            & (results["Number of characteristics"] == int(nr))
        ]
        chronological.append(
            float(temp[temp["Split type"] == "chronological"][measure_type])
        )
        random.append(float(temp[temp["Split type"] == "random"][measure_type]))

    br1 = np.arange(len(chronological))
    br2 = [x + bar_width for x in br1]

    plt.bar(
        br1,
        chronological,
        color="r",
        width=bar_width,
        edgecolor="grey",
        label="chronological",
    )
    plt.bar(br2, random, color="g", width=bar_width, edgecolor="grey", label="random")

    plt.xlabel("Split type & nr of characteristics", fontweight="bold", fontsize=25)
    plt.ylabel(measure_type, fontweight="bold", fontsize=25)
    plt.xticks([r + bar_width for r in range(len(chronological))], labels, fontsize=20)

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment="right")
    plt.legend(fontsize=20)
    plt.show()


def plot_one_type_split(results, split_type, measure_type, figsize=(20, 8)):
    bar_width = 0.25
    fig, ax = plt.subplots(figsize=figsize)
    ax.grid()
    fig.autofmt_xdate()
    plt.grid(axis="y", linestyle="--")
    data = results[results["Split type"] == split_type]

    labels = data.apply(
        lambda row: row["Tuning type"] + " " + str(row["Number of characteristics"]),
        axis="columns",
    )
    values = []

    for i, l in enumerate(labels):
        t, nr = l.split(" ")
        temp = data[
            (data["Tuning type"] == t) & (data["Number of characteristics"] == int(nr))
        ]
        values.append(float(temp[measure_type]))

    plt.bar(labels, values, width=bar_width)

    plt.xlabel("Split type & nr of characteristics", fontweight="bold", fontsize=25)
    plt.ylabel(measure_type, fontweight="bold", fontsize=25)
    plt.xticks([r + bar_width for r in range(len(values))], labels, fontsize=20)

    plt.show()
