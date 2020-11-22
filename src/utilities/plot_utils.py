""" Utilities for plotting.

This modules contains standardized functions for plotting
 different types of graphs used throughout the project.


"""
#####################################################
# IMPORTS
#####################################################
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#####################################################
# PARAMETERS
#####################################################

markers = [".", "^", "x", "o", "+", "*", "p", "D", "s", "8", "2", "h", "d"]
linestyles = [
    (0, ()),
    (0, (1, 1)),
    (0, (5, 1)),
    (0, (5, 1, 1, 1)),
    (0, (3, 5, 1, 5, 1, 5)),
    (0, (1, 10)),
    (0, (5, 10)),
    (0, (5, 1, 10, 1)),
    (0, (3, 10, 1, 10, 1, 10)),
    (0, (1, 15)),
    (0, (5, 15)),
    (0, (5, 1, 15, 1)),
    (0, (3, 15, 1, 15, 1, 15)),
]
colors = ["tab:blue", "tab:orange", "tab:red", "gold", "limegreen", "deeppink"]


#####################################################
# FUNCTIONS
#####################################################


def _plot_development_over_time(data, params):

    # collect data
    plot_x = data["date"]
    plot_y = np.array(
        [
            data["new_cases_week_per_100k"],
            data["new_tests_week_per_100k"],
            data["positive_rate_week"],
            data["new_cases_7d_per_100k"],
            data["new_tests_7d_per_100k"],
            data["positive_rate_7d"],
            data["new_cases_14d_per_100k"],
            data["new_tests_14d_per_100k"],
            data["positive_rate_14d"],
        ],
    )

    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(15, 15))

    fig.suptitle(params["title"], y=1.0)
    ax[0, 0].plot(plot_x, plot_y[0])
    ax[0, 0].set_title("new cases per week per 100k inhabitants")
    ax[1, 0].plot(plot_x, plot_y[1])
    ax[1, 0].set_title("new tests per week per 100k inhabitants")
    ax[2, 0].plot(plot_x, plot_y[2])
    ax[2, 0].set_title("positive rate in per week")
    ax[0, 1].plot(plot_x, plot_y[3])
    ax[0, 1].set_title("new cases in the last 7 days per 100k inhabitants")
    ax[1, 1].plot(plot_x, plot_y[4])
    ax[1, 1].set_title("new tests in the last 7 days per 100k inhabitants")
    ax[2, 1].plot(plot_x, plot_y[5])
    ax[2, 1].set_title("positive rate in the last 7 days")
    ax[0, 2].plot(plot_x, plot_y[6])
    ax[0, 2].set_title("new cases in the last 14 days per 100k inhabitants")
    ax[1, 2].plot(plot_x, plot_y[7])
    ax[1, 2].set_title("new tests in the last 14 days per 100k inhabitants")
    ax[2, 2].plot(plot_x, plot_y[8])
    ax[2, 2].set_title("positive rate in the last 14 days")

    for row in range(ax.shape[0]):
        for col in range(ax.shape[1]):
            ax[row, col].xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
            ax[row, col].xaxis.set_minor_formatter(mdates.DateFormatter("%d.%m"))
            ax[row, col].set_xlim((plot_x[0], plot_x[-1]))
            plt.setp(ax[row, col].xaxis.get_majorticklabels(), rotation=90)

    fig.savefig(params["outpath"])


def _plot_stacked_area_100(data, params):

    try:
        figsize = params["figsize"]
    except KeyError:
        figsize = (12, 6)

    x = pd.to_datetime(data.index)

    fig, ax = plt.subplots(figsize=figsize)

    ax.stackplot(
        x,
        data.T,
        labels=data.columns,
        alpha=0.2,
        # colors=colors,
    )

    for idx in range(data.shape[1] - 1):
        ax.plot(
            x, data.cumsum(axis=1).iloc[:, idx], color="dimgray", linestyle="dotted",
        )

    # format axes
    ax.set_xlim(pd.to_datetime([data.index[0], data.index[-1]]))
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b \n %Y"))

    # format plot area
    ax.margins(0, 0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # save figure
    fig.savefig(params["outpath"])
    plt.close()
