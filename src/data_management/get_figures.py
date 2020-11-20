import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from bld.project_paths import project_paths_join as ppj

#######################
# FUNCTIONS
#######################


def plot_development_over_time(input_data):

    # collect data
    plot_x = input_data["date"]
    plot_y = np.array(
        [
            input_data["new_cases_week_per_100k"],
            input_data["new_tests_week_per_100k"],
            input_data["positive_rate_week"],
            input_data["new_cases_7d_per_100k"],
            input_data["new_tests_7d_per_100k"],
            input_data["positive_rate_7d"],
            input_data["new_cases_14d_per_100k"],
            input_data["new_tests_14d_per_100k"],
            input_data["positive_rate_14d"],
        ],
    )
    iso_code = input_data.iso_code.unique().item()

    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(15, 15))

    fig.suptitle(f"Cases and tests ({country})", y=1.0)
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

    fig.savefig(ppj("OUT_FIGURES", "covid_time_series_" + iso_code + ".pdf"))


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


#######################
# SCRIPT
#######################

if __name__ == "__main__":

    idx = pd.IndexSlice

    owid_dtypes = {
        "iso_code": str,
        "continent": str,
        "location": str,
        "total_cases": float,
        "new_cases": float,
        "new_cases_smoothed": float,
        "total_deaths": float,
        "new_deaths": float,
        "new_deaths_smoothed": float,
        "total_cases_per_million": float,
        "new_cases_per_million": float,
        "new_cases_smoothed_per_million": float,
        "total_deaths_per_million": float,
        "new_deaths_per_million": float,
        "new_deaths_smoothed_per_million": float,
        "total_tests": float,
        "new_tests": float,
        "total_tests_per_thousand": float,
        "new_tests_per_thousand": float,
        "new_tests_smoothed": float,
        "new_tests_smoothed_per_thousand": float,
        "tests_per_case": float,
        "positive_rate": float,
        "tests_units": str,
        "stringency_index": float,
        "population": float,
        "population_density": float,
        "median_age": float,
        "aged_65_older": float,
        "aged_70_older": float,
        "gdp_per_capita": float,
        "extreme_poverty": float,
        "cardiovasc_death_rate": float,
        "diabetes_prevalence": float,
        "female_smokers": float,
        "male_smokers": float,
        "handwashing_facilities": float,
        "hospital_beds_per_thousand": float,
        "life_expectancy": float,
        "human_development_index": float,
    }
    # url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    # IN_DATA = "data/"
    #
    # file_name_data = "COVID-19-geographic-disbtribution-worldwide.csv"
    # file_name_codes = "country_and_continent_codes.csv"
    #
    # # get data from server and store locally
    # my_file = requests.get(url)
    # open(IN_DATA + file_name_data, "wb").write(my_file.content)
    #
    # # load data floato data frame
    # analysis_df = pd.read_csv(IN_DATA + file_name_data)
    country_codes = pd.read_csv(ppj("IN_DATA", "country_and_continent_codes.csv"))

    analysis_df = pd.read_csv(
        ppj("IN_DATA_OWID", "owid-covid-data.csv"),
        dtype=owid_dtypes,
        parse_dates=["date"],
    )
    divi_df = pd.read_csv(
        ppj("IN_DATA", "divi_data.csv"), parse_dates=["date"], dtype=float
    )
    divi_df.index = divi_df.date

    # add variables
    divi_df.loc[:, "ICU_covid_ventilated"] = divi_df.total_cases_ventilated
    divi_df.loc[:, "ICU_covid_not_ventilated"] = (
        divi_df.total_cases_hospitalized - divi_df.total_cases_ventilated
    )
    divi_df.loc[:, "ICU_other"] = (
        divi_df.beds_occupied - divi_df.total_cases_hospitalized
    )
    divi_df.loc[:, "ICU_vacant"] = divi_df.beds_vacant
    divi_df.loc[:, "ICU_capacity"] = divi_df.beds_vacant + divi_df.beds_occupied

    # drop double entries
    country_codes.drop(
        country_codes[
            np.logical_and(
                country_codes.Country_Name == "Azerbaijan, Republic of",
                country_codes.Continent_Name == "Europe",
            )
        ].index,
        inplace=True,
    )
    country_codes.drop(
        country_codes[
            np.logical_and(
                country_codes.Country_Name == "Armenia, Republic of",
                country_codes.Continent_Name == "Europe",
            )
        ].index,
        inplace=True,
    )
    country_codes.drop(
        country_codes[
            np.logical_and(
                country_codes.Country_Name == "Cyprus, Republic of",
                country_codes.Continent_Name == "Asia",
            )
        ].index,
        inplace=True,
    )
    country_codes.drop(
        country_codes[
            np.logical_and(
                country_codes.Country_Name == "Georgia",
                country_codes.Continent_Name == "Europe",
            )
        ].index,
        inplace=True,
    )
    country_codes.drop(
        country_codes[
            np.logical_and(
                country_codes.Country_Name == "Kazakhstan, Republic of",
                country_codes.Continent_Name == "Europe",
            )
        ].index,
        inplace=True,
    )
    country_codes.drop(
        country_codes[
            np.logical_and(
                country_codes.Country_Name == "United States Minor Outlying Islands",
                country_codes.Continent_Name == "Oceania",
            )
        ].index,
        inplace=True,
    )
    country_codes.drop(
        country_codes[
            np.logical_and(
                country_codes.Country_Name == "Russian Federation",
                country_codes.Continent_Name == "Asia",
            )
        ].index,
        inplace=True,
    )
    country_codes.drop(
        country_codes[
            np.logical_and(
                country_codes.Country_Name == "Turkey, Republic of",
                country_codes.Continent_Name == "Europe",
            )
        ].index,
        inplace=True,
    )

    # sort data
    analysis_df = analysis_df.sort_values(by=["iso_code", "date"])

    analysis_df.index = pd.MultiIndex.from_arrays(
        [analysis_df.date, analysis_df.iso_code], names=("date", "iso_code"),
    )
    analysis_df.index = pd.MultiIndex.from_arrays(
        [
            analysis_df.index.get_level_values(0).date,
            analysis_df.index.get_level_values(1),
        ]
    )

    analysis_df.loc[idx[:, "DEU"], "new_tests"] = analysis_df.loc[
        idx[:, "DEU"], "total_tests"
    ].diff(periods=7)

    analysis_df.loc[:, "new_cases_7d"] = analysis_df.new_cases.rolling(
        window=7, on=analysis_df.index.levels[0]
    ).sum()
    analysis_df.loc[
        analysis_df.groupby(axis=0, level=1).head(6).index, "new_cases_7d"
    ] = np.nan

    analysis_df.loc[:, "new_cases_7d_per_100k"] = (
        analysis_df.new_cases_7d / analysis_df.population * 1e5
    )

    tmp_df = pd.merge(
        analysis_df.new_cases.groupby(
            [analysis_df.date.dt.isocalendar().week, analysis_df.iso_code]
        ).sum(min_count=1),
        analysis_df.new_tests.groupby(
            [analysis_df.date.dt.isocalendar().week, analysis_df.iso_code]
        ).sum(min_count=1),
        how="outer",
        left_index=True,
        right_index=True,
    )

    tmp_df = tmp_df.rename(
        columns={"new_cases": "new_cases_week", "new_tests": "new_tests_week"}
    )

    analysis_df = pd.merge(
        analysis_df,
        tmp_df,
        how="left",
        left_on=[
            analysis_df.date.dt.isocalendar().week.astype(str),
            analysis_df.iso_code.astype(str),
        ],
        right_on=[
            tmp_df.index.get_level_values(0).astype(str),
            tmp_df.index.get_level_values(1).astype(str),
        ],
    )

    analysis_df.index = pd.MultiIndex.from_arrays(
        [analysis_df.date, analysis_df.iso_code], names=("date", "iso_code"),
    )
    analysis_df.index = pd.MultiIndex.from_arrays(
        [
            analysis_df.index.get_level_values(0).date,
            analysis_df.index.get_level_values(1),
        ]
    )

    analysis_df.loc[:, "new_cases_week_per_100k"] = (
        analysis_df.new_cases_week / analysis_df.population * 1e5
    )

    analysis_df.loc[:, "new_tests_week_per_100k"] = (
        analysis_df.new_tests_week / analysis_df.population * 1e5
    )

    analysis_df.loc[:, "new_cases_14d"] = analysis_df.new_cases.rolling(
        window=14, on=analysis_df.index.levels[0]
    ).sum()
    analysis_df.loc[
        analysis_df.groupby(axis=0, level=1).head(13).index, "new_cases_14d"
    ] = np.nan

    analysis_df.loc[:, "new_cases_14d_per_100k"] = (
        analysis_df.new_cases_14d / analysis_df.population * 1e5
    )

    analysis_df.loc[:, "new_tests_7d"] = analysis_df.new_tests.rolling(
        window=7, on=analysis_df.index.levels[0]
    ).sum()
    analysis_df.loc[
        analysis_df.groupby(axis=0, level=1).head(6).index, "new_tests_7d"
    ] = np.nan

    analysis_df.loc[:, "new_tests_14d"] = analysis_df.new_tests.rolling(
        window=14, on=analysis_df.index.levels[0]
    ).sum()
    analysis_df.loc[
        analysis_df.groupby(axis=0, level=1).head(13).index, "new_tests_14d"
    ] = np.nan

    analysis_df.loc[:, "new_tests_7d_per_100k"] = (
        analysis_df.new_tests_7d / analysis_df.population * 1e5
    )

    analysis_df.loc[:, "new_tests_14d_per_100k"] = (
        analysis_df.new_tests_14d / analysis_df.population * 1e5
    )

    analysis_df.loc[:, "positive_rate_7d"] = (
        analysis_df.new_cases_7d / analysis_df.new_tests_7d
    )

    analysis_df.loc[:, "positive_rate_14d"] = (
        analysis_df.new_cases_14d / analysis_df.new_tests_14d
    )

    analysis_df.loc[:, "positive_rate_week"] = (
        analysis_df.new_cases_week / analysis_df.new_tests_week
    )

    # countries = [
    #     "USA",
    #     "DEU",
    #     "FRA",
    #     "ITA",
    #     "ESP",
    #     "LBN",
    #     "JOR",
    #     "TUR",
    #     "IRQ",
    #     "SYR",
    #     "PAK",
    #     "AFG",
    #     "KEN",
    #     "ETH",
    #     "UGA",
    #     "COL",
    #     "PAK",
    #     "BRA",
    # ]
    countries = ["DEU", "FRA", "USA", "ESP", "ITA", "BEL"]

    plot_data = pd.DataFrame(
        data=divi_df.loc[
            :,
            [
                "ICU_covid_ventilated",
                "ICU_covid_not_ventilated",
                "ICU_other",
                "ICU_vacant",
            ],
        ]
    )
    plot_params = {
        "figsize": (8, 16 / 3),
        "outpath": ppj("OUT_FIGURES", "divi_icu_time_series.pdf"),
    }
    _plot_stacked_area_100(plot_data, plot_params)

    for country in countries:
        country_data = analysis_df[analysis_df["iso_code"] == country]
        plot_development_over_time(country_data)
