import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
)


def print_check_predictions(y: pd.Series, y_pred: np.ndarray) -> None:
    """
    Calculate and print RMSE for predicted values.

    :param y: True values.
    :param y_pred: Predicted values from a model.
    :return: None
    """
    print(f"RMSE: {mean_squared_error(y, y_pred, squared=False):.2f}\n")


def round_predictions(predict: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """
    Round predicted values based on a specified threshold.

    Values above the threshold are rounded up, and values below are rounded down.

    :param predict: Predicted values to be rounded.
    :param threshold: A round type threshold as a float between 0 and 1. Default is 0.5.
    :return: Rounded values with a maximum value of 21.
    """
    if threshold > 1 or threshold < 0:
        raise ValueError(f"Incorrect threshold value: {threshold}")
    threshold_predict = np.where(
        (predict % 1) > threshold, np.ceil(predict), np.floor(predict)
    ).astype("int")

    return np.where(threshold_predict > 20, 21, threshold_predict)


def evaluate_round_predictions(
    round_types: list[float], y: pd.Series, predict: np.ndarray
) -> None:
    """
    Evaluate and print the predictions of a model at different round thresholds,
    including a normal prediction (no rounding), and for each threshold specified in the 'round_types' list.

    :param round_types: A list of round thresholds specified as a list of floats.
    :param y: True values.
    :param predict: Predicted values from the model.
    :return: None
    """
    print("Default:")
    print_check_predictions(y, predict)

    for threshold in round_types:
        threshold_predict = round_predictions(predict, threshold)

        print(f"Round type: {threshold}")
        print_check_predictions(y, threshold_predict)


def plot_mae_by_level(
    y_test: pd.Series,
    y_pred_test: np.ndarray,
    title: str = None,
    figsize: tuple[int, int] = (20, 8),
    export: bool = False,
) -> None:
    """
    Plots Mean Absolute Error (MAE) by level.

    Calculates MAE for each level and displays the value on a bar chart.

    :param y_test: True values.
    :param y_pred_test: Predicted values.
    :param title: Plot title.
    :param figsize: A tuple specifying the figure size (width, height). Default is (20, 8).
    :param export: If true, saves plot to results_diagrams file. Default is False.
    :return: None
    """

    y_test = y_test.reset_index(drop=True)
    level_max = y_test.max()

    mae_by_level = pd.DataFrame(columns=["level", "mae"])
    for lvl in range(-1, level_max + 1):
        y_test_curr = y_test[y_test == lvl]
        y_pred_test_curr = pd.DataFrame(y_pred_test)[y_test == lvl]

        mae = mean_absolute_error(y_test_curr, y_pred_test_curr)
        mae_by_level.loc[lvl + 1] = [lvl, mae]

    fig, ax = plt.subplots(figsize=figsize)
    # plt.figure(figsize=figsize)
    plt.bar(mae_by_level["level"], mae_by_level["mae"])
    plt.xlabel("Level", fontweight="bold", fontsize=20)
    plt.ylabel("Mean Absolute Error (MAE)", fontweight="bold", fontsize=20)

    if title is None:
        plt.title("MAE by level", fontsize=23, fontweight="bold")
    else:
        plt.title(title, fontsize=23, fontweight="bold")

    plt.xticks(mae_by_level["level"])

    fig.tight_layout()
    if export:
        plt.savefig(f"../results_diagrams/other/mae_by_level/{title}.svg")

    plt.show()


def plot_confusion_matrix(
    predict: np.ndarray,
    y: pd.Series,
    threshold: float = 0.5,
    title: str = None,
    figsize: tuple[int, int] = (10, 10),
    export: bool = False,
) -> None:
    """
    Plots a confusion matrix for rounded predictions based on a specified threshold.
    It visualizes the confusion matrix using a heatmap.

    :param predict: Predicted values to be rounded.
    :param y: True values.
    :param threshold: A round type threshold as a float between 0 and 1. Default is 0.5.
    :param title: Plot title.
    :param figsize: A tuple specifying the figure size (width, height). Default is (10, 10).
    :param export: If true, saves plot to results_diagrams file. Default is False.
    :return: None
    """
    round_predict = round_predictions(predict, threshold)
    cm = confusion_matrix(y, round_predict)

    # min possible level: -1, max possible level: 21
    labels = [i for i in range(-1, 22)]

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

    fig, ax = plt.subplots(figsize=figsize)
    disp.plot(ax=ax, colorbar=False)

    # Adding custom colorbar
    cax = fig.add_axes(
        [
            ax.get_position().x1 + 0.01,
            ax.get_position().y0,
            0.02,
            ax.get_position().height,
        ]
    )
    plt.colorbar(disp.im_, cax=cax)

    disp.ax_.set_xlabel("Predicted level", fontweight="bold", fontsize=20)
    disp.ax_.set_ylabel("True level", fontweight="bold", fontsize=20)

    if title is None:
        disp.ax_.set_title("Confusion matrix", fontweight="bold", fontsize=20)
    else:
        disp.ax_.set_title(title, fontweight="bold", fontsize=20)

    if export:
        title = title.replace("\n", " ")
        fig.savefig(
            f"../results_diagrams/other/confusion_matrix/{title}.svg",
            bbox_inches="tight",
        )

    plt.show()


def assess_regression_model(
    model,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    r2: bool = False,
) -> tuple[float, float]:
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
    :return: Tuple of RMSE and MAE for the test data.
    """

    # predict for train and test
    y_pred_test = model.predict(X_test)
    y_pred_train = model.predict(X_train)

    # calculate train and test RMSE, MSE and MAE
    rmse_train = mean_squared_error(y_train, y_pred_train, squared=False)
    rmse_test = mean_squared_error(y_test, y_pred_test, squared=False)
    mae_test = mean_absolute_error(y_test, y_pred_test)

    if r2:
        # calculate R2
        r2 = model.score(X_train, y_train)
        print(f"R2: {r2:.2f}")

    # print train and test RMSE
    print(f"RMSE train: {rmse_train:.2f}")
    print(f"RMSE test: {rmse_test:.2f}")
    print(f"MAE test: {mae_test:.2f}\n")

    return rmse_test, mae_test


def plot_summary(
    results: pd.DataFrame,
    measure_type: str,
    title: str = None,
    figsize: tuple[int, int] = (20, 8),
    export: bool = False,
) -> None:
    """
    Plot a summary bar chart of evaluation metrics for different model tuning types and characteristics.

    It displays a bar chart to visualize the performance of models for a specified 'measure_type'
    under different conditions.


    :param results: A DataFrame with evaluation results, including 'Tuning type', 'Split type',
    'Set of features', and the 'measure_type' of interest.
    :param measure_type: The evaluation metric to be displayed on the y-axis (e.g., "RMSE", "MSE").
    :param title: Plot tile.
    :param figsize: A tuple specifying the figure size (width, height). Default is (20, 8).
    :param export: If true, saves plot to results_diagrams file. Default is False.
    :return: None
    """

    bar_width = 0.25
    fig, ax = plt.subplots(1, figsize=figsize)
    ax.grid()
    fig.autofmt_xdate()
    plt.grid(axis="y", linestyle="--")

    labels = results.apply(
        lambda row: row["Tuning type"] + " " + str(row["Set of features"]),
        axis="columns",
    )
    labels = dict.fromkeys(labels).keys()
    chronological = []
    random = []

    for i, l in enumerate(labels):
        t, no = l.split(" ")
        temp = results[
            (results["Tuning type"] == t) & (results["Set of features"] == no)
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

    plt.xlabel("Tuning type & set of features", fontweight="bold", fontsize=25)
    plt.ylabel(measure_type, fontweight="bold", fontsize=25)
    plt.xticks([r + bar_width for r in range(len(chronological))], labels, fontsize=20)

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment="right")
    plt.legend(fontsize=20, title="Split type", title_fontsize=20)

    if title is None:
        plt.title(
            f"Summary of {measure_type} for Different Model Tuning Types and Characteristics",
            fontsize=30,
            fontweight="bold",
        )
    else:
        plt.title(title, fontsize=30, fontweight="bold")

    fig.tight_layout()
    if export:
        plt.savefig(f"../results_diagrams/rmse_and_mae/{title}.svg")

    plt.show()


def plot_one_type_split(
    results: pd.DataFrame,
    split_type: str,
    measure_type: str,
    title: str = None,
    figsize: tuple[int, int] = (20, 8),
) -> None:
    """
    Plot a summary bar chart of evaluation metrics for a specific split type and measure type.

    It displays a bar chart to visualize the performance of models for a specified 'split_type' and
    'measure_type' under different conditions.

    :param results: A DataFrame with evaluation results, including 'Tuning type', 'Split type',
    'Set of features', and the 'measure_type' of interest.
    :param split_type: The type of data split (e.g., "chronological," "random") for which you want to visualize the evaluation metrics.
    :param measure_type: The evaluation metric to be displayed on the y-axis (e.g., "RMSE", "MSE").
    :param title: Plot title.
    :param figsize: A tuple specifying the figure size (width, height). Default is (20, 8).
    :return: None
    """

    bar_width = 0.25
    fig, ax = plt.subplots(figsize=figsize)
    ax.grid()
    fig.autofmt_xdate()
    plt.grid(axis="y", linestyle="--")
    data = results[results["Split type"] == split_type]

    labels = data.apply(
        lambda row: row["Tuning type"] + " " + str(row["Set of features"]),
        axis="columns",
    )
    values = []

    for i, l in enumerate(labels):
        t, no = l.split(" ")
        temp = data[(data["Tuning type"] == t) & (data["Set of features"] == no)]
        values.append(float(temp[measure_type]))

    plt.bar(labels, values, width=bar_width)

    plt.xlabel("Tuning type & set of features", fontweight="bold", fontsize=25)
    plt.ylabel(measure_type, fontweight="bold", fontsize=25)
    plt.xticks([r + bar_width for r in range(len(values))], labels, fontsize=20)

    if title is None:
        plt.title(
            f"Summary of {measure_type} for {split_type} Split Type and Different Model Tuning Types and Characteristics",
            fontsize=30,
            fontweight="bold",
        )
    else:
        plt.title(title, fontsize=30, fontweight="bold")

    plt.show()


def plot_summary_all_models(
    results: pd.DataFrame,
    split_type: str,
    measure_type: str,
    title: str = None,
    figsize: tuple[int, int] = (20, 8),
    export: bool = False,
) -> None:
    """
    Plot a summary bar chart of evaluation metrics for different models, model tuning types and characteristics.

    It displays a bar chart to visualize the performance of different machine learning models,
    for a specified 'split_type' and 'measure_type' under different conditions.


    :param results: A DataFrame with evaluation results, including 'Tuning type', 'Split type',
    'Set of features', and the 'measure_type' of interest.
    :param split_type: The type of data split (e.g., "chronological," "random") for which you want to visualize the evaluation metrics.
    :param measure_type: The evaluation metric to be displayed on the y-axis (e.g., "RMSE", "MSE").
    :param title: Plot title.
    :param figsize: A tuple specifying the figure size (width, height). Default is (20, 8).
    :param export: If true, saves plot to results_diagrams file. Default is False.
    :return: None
    """

    bar_width = 0.25
    fig, ax = plt.subplots(1, figsize=figsize)
    ax.grid()
    fig.autofmt_xdate()
    plt.grid(axis="y", linestyle="--")
    data = results[results["Split type"] == split_type]

    labels = data.apply(
        lambda row: row["Tuning type"] + " " + str(row["Set of features"]),
        axis="columns",
    )
    labels = dict.fromkeys(labels).keys()
    linear_regression = []
    random_forest = []
    lightgbm = []

    for i, l in enumerate(labels):
        t, no = l.split(" ")
        temp = data[(data["Tuning type"] == t) & (data["Set of features"] == no)]
        linear_regression.append(
            float(temp[temp["Model type"] == "Linear Regression"][measure_type])
        )
        random_forest.append(
            float(temp[temp["Model type"] == "Random Forest"][measure_type])
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
        label="Linear Regression",
    )
    plt.bar(
        br2,
        random_forest,
        color="g",
        width=bar_width,
        edgecolor="grey",
        label="Random Forest",
    )
    plt.bar(
        br3, lightgbm, color="b", width=bar_width, edgecolor="grey", label="LightGBM"
    )

    plt.xlabel("Tuning type & set of features", fontweight="bold", fontsize=25)
    plt.ylabel(measure_type, fontweight="bold", fontsize=25)
    plt.xticks(
        [r + bar_width for r in range(len(linear_regression))], labels, fontsize=20
    )

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment="right")
    plt.legend(fontsize=20, title="Model", title_fontsize=20)

    if title is None:
        plt.title(
            f"Summary of {measure_type} for {split_type} Split Type and Different Models, Tuning Types, and Characteristics",
            fontsize=30,
            fontweight="bold",
        )
    else:
        plt.title(title, fontsize=30, fontweight="bold")

    fig.tight_layout()
    if export:
        plt.savefig(f"results_diagrams/rmse_and_mae/summary/{title}.svg")

    plt.show()
