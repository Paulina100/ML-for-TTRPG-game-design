import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
)


def print_check_predictions(y, y_pred):
    """
    Calculate and print MSE and RMSE for predicted values.

    :param y: True values.
    :param y_pred: Predicted values from a model.
    """
    print(f"MSE: {mean_squared_error(y, y_pred):.2f}")
    print(f"RMSE: {mean_squared_error(y, y_pred, squared=False):.2f}\n")


def round_predictions(threshold: str | float, predict):
    """
    Round predicted values based on a specified threshold.

    If threshold is a string "round", it rounds normally.
    If 'threshold' is a float, values above the threshold are rounded up, and values below are rounded down.

    :param threshold: A round type threshold as a string ("round") or a float between 0 and 1.
    :param predict: Predicted values to be rounded.
    :return: Rounded values with a maximum value of 21.
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
    Evaluate and print the predictions of a model at different round thresholds,
    including a normal prediction (no rounding), and for each threshold specified in the 'round_types' list.

    :param round_types: A list of round thresholds specified as a list of strings or floats.
    :param y: True values.
    :param predict: Predicted values from the model.
    """
    print("Normal:")
    print_check_predictions(y, predict)

    for threshold in round_types:
        threshold_predict = round_predictions(threshold, predict)

        print(f"Round type: {threshold}")
        print_check_predictions(y, threshold_predict)


def plot_confusion_matrix(threshold, predict, y):
    """
    Plot a confusion matrix for rounded predictions based on a specified threshold.
    It visualizes the confusion matrix using a heatmap.

    :param threshold: A round type threshold as a string ("round") or a float between 0 and 1.
    :param predict: Predicted values to be rounded.
    :param y: True values.
    """
    round_predict = round_predictions(threshold, predict)
    cm = confusion_matrix(y, round_predict)

    # min possible level: -1, max possible level: 21
    labels = [i for i in range(-1, 22)]

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

    disp.plot()
    plt.title("Confusion matrix")
    plt.show()


def assess_regression_model(model, X_train, X_test, y_train, y_test, r2=False):
    """
    Assess the performance of a regression model and print evaluation metrics.

    Calculates and prints evaluation metrics.
    The metrics include: RMSE for training data, RMSE for testing data, MSE for testing data, and MAE for testing data.
    Optionally, calculates and prints the R2 coefficient for the training data.

    :param model: A trained regression model.
    :param X_train: Training data.
    :param X_test: Testing data.
    :param y_train: True values for the training data.
    :param y_test: True values for the testing data.
    :param r2: If True, calculate and print the R2 coefficient for the training data.
    :return: Tuple of RMSE, MSE and MAE for the test data.
    """

    # predict for train and test
    y_pred_test = model.predict(X_test)
    y_pred_train = model.predict(X_train)

    # calculate train and test RMSE, MSE and MAE
    rmse_train = mean_squared_error(y_train, y_pred_train, squared=False)
    rmse_test = mean_squared_error(y_test, y_pred_test, squared=False)
    mse_test = mean_squared_error(y_test, y_pred_test)
    mae_test = mean_absolute_error(y_test, y_pred_test)

    if r2:
        # calculate R2
        r2 = model.score(X_train, y_train)
        print(f"R2: {r2:.2f}")

    # print train and test RMSE
    print(f"RMSE train: {rmse_train:.2f}")
    print(f"RMSE test: {rmse_test:.2f}")
    print(f"MSE test: {mse_test:.2f}")
    print(f"MAE test: {mae_test:.2f}\n")

    return rmse_test, mse_test, mae_test


def plot_summary(results, measure_type, figsize=(20, 8)):
    """
    Plot a summary bar chart of evaluation metrics for different model tuning types and characteristics.

    It displays a bar chart to visualize the performance of models for a specified 'measure_type'
    under different conditions.


    :param results: A DataFrame with evaluation results, including 'Tuning type', 'Split type',
    'Number of characteristics', and the 'measure_type' of interest.
    :param measure_type: The evaluation metric to be displayed on the y-axis (e.g., "RMSE", "MSE").
    :param figsize: A tuple specifying the figure size (width, height). Default is (20, 8).
    """

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
    """
    Plot a summary bar chart of evaluation metrics for a specific split type and measure type.

    It displays a bar chart to visualize the performance of models for a specified 'split_type' and
    'measure_type' under different conditions.

    :param results: A DataFrame with evaluation results, including 'Tuning type', 'Split type',
    'Number of characteristics', and the 'measure_type' of interest.
    :param split_type: The type of data split (e.g., "chronological," "random") for which you want to visualize the evaluation metrics.
    :param measure_type: The evaluation metric to be displayed on the y-axis (e.g., "RMSE", "MSE").
    :param figsize: A tuple specifying the figure size (width, height). Default is (20, 8).
    """

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


def plot_summary_all_models(results, split_type, measure_type, figsize=(20, 8)):
    """
    Plot a summary bar chart of evaluation metrics for different models, model tuning types and characteristics.

    It displays a bar chart to visualize the performance of different machine learning models,
    for a specified 'split_type' and 'measure_type' under different conditions.


    :param results: A DataFrame with evaluation results, including 'Tuning type', 'Split type',
    'Number of characteristics', and the 'measure_type' of interest.
    :param split_type: The type of data split (e.g., "chronological," "random") for which you want to visualize the evaluation metrics.
    :param measure_type: The evaluation metric to be displayed on the y-axis (e.g., "RMSE", "MSE").
    :param figsize: A tuple specifying the figure size (width, height). Default is (20, 8).
    """

    bar_width = 0.25
    fig, ax = plt.subplots(1, figsize=figsize)
    ax.grid()
    fig.autofmt_xdate()
    plt.grid(axis="y", linestyle="--")
    data = results[results["Split type"] == split_type]

    labels = data.apply(
        lambda row: row["Tuning type"] + " " + str(row["Number of characteristics"]),
        axis="columns",
    )
    labels = dict.fromkeys(labels).keys()
    linear_regression = []
    random_forest = []
    lightgbm = []

    for i, l in enumerate(labels):
        t, nr = l.split(" ")
        temp = data[
            (data["Tuning type"] == t) & (data["Number of characteristics"] == int(nr))
        ]
        linear_regression.append(
            float(temp[temp["Model type"] == "Linear regression"][measure_type])
        )
        random_forest.append(
            float(temp[temp["Model type"] == "Random forest"][measure_type])
        )
        lightgbm.append(float(temp[temp["Model type"] == "LightGBM"][measure_type]))

    br1 = np.arange(len(linear_regression))
    br2 = [x + bar_width for x in br1]
    br3 = [x + bar_width for x in br2]

    plt.bar(
        br1,
        linear_regression,
        color="r",
        width=bar_width,
        edgecolor="grey",
        label="Linear regression",
    )
    plt.bar(
        br2,
        random_forest,
        color="g",
        width=bar_width,
        edgecolor="grey",
        label="Random forest",
    )
    plt.bar(
        br3, lightgbm, color="b", width=bar_width, edgecolor="grey", label="LightGBM"
    )

    plt.xlabel("Tuning type & nr of characteristics", fontweight="bold", fontsize=25)
    plt.ylabel(measure_type, fontweight="bold", fontsize=25)
    plt.xticks(
        [r + bar_width for r in range(len(linear_regression))], labels, fontsize=20
    )

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment="right")
    plt.legend(fontsize=20)
    plt.show()
