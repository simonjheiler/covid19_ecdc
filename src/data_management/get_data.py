import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

from bld.project_paths import project_paths_join as ppj

#######################
# FUNCTIONS
#######################


def plot_development_over_time(input_data):

    # collect data
    plot_x = input_data["date"]
    plot_y = np.array(
        [
            input_data["total_cases"],
            input_data["new_cases"],
            input_data["total_deaths"],
            input_data["new_deaths"],
            input_data["new_cases_7d_per_100k"],
            input_data["new_cases_14d_per_100k"],
        ],
    )

    fig, ax = plt.subplots(nrows=3, ncols=2)

    fig.suptitle(f"Case and death count ({country})", y=1.0)
    ax[0, 0].plot(plot_x, plot_y[0])
    ax[0, 0].set_title("Cases (cumulative)")
    ax[0, 0].set_yscale("log")
    ax[1, 0].plot(plot_x, plot_y[1])
    ax[1, 0].set_title("Cases (daily increase)")
    ax[2, 0].plot(plot_x, plot_y[4])
    ax[2, 0].set_title("7-day incidence")
    ax[0, 1].plot(plot_x, plot_y[2])
    ax[0, 1].set_title("Deaths (cumulative)")
    ax[0, 1].set_yscale("log")
    ax[1, 1].plot(plot_x, plot_y[3])
    ax[1, 1].set_title("Deaths (daily increase)")
    ax[2, 1].plot(plot_x, plot_y[5])
    ax[2, 1].set_title("14-day incidence")

    for row in range(ax.shape[0]):
        for col in range(ax.shape[1]):
            ax[row, col].xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
            ax[row, col].xaxis.set_minor_formatter(mdates.DateFormatter("%d.%m"))
            plt.setp(ax[row, col].xaxis.get_majorticklabels(), rotation=90)

    plt.show()


#######################
# SCRIPT
#######################

if __name__ == "__main__":


    owid_dtypes = {
        'iso_code': str,
        'continent': str,
        'location': str,
        'total_cases': float,
        'new_cases': float,
        'new_cases_smoothed': float,
        'total_deaths': float,
        'new_deaths': float,
        'new_deaths_smoothed': float,
        'total_cases_per_million': float,
        'new_cases_per_million': float,
        'new_cases_smoothed_per_million': float,
        'total_deaths_per_million': float,
        'new_deaths_per_million': float,
        'new_deaths_smoothed_per_million': float,
        'total_tests': float,
        'new_tests': float,
        'total_tests_per_thousand': float,
        'new_tests_per_thousand': float,
        'new_tests_smoothed': float,
        'new_tests_smoothed_per_thousand': float,
        'tests_per_case': float,
        'positive_rate': float,
        'tests_units': str,
        'stringency_index': float,
        'population': float,
        'population_density': float,
        'median_age': float,
        'aged_65_older': float,
        'aged_70_older': float,
        'gdp_per_capita': float,
        'extreme_poverty': float,
        'cardiovasc_death_rate': float,
        'diabetes_prevalence': float,
        'female_smokers': float,
        'male_smokers': float,
        'handwashing_facilities': float,
        'hospital_beds_per_thousand': float,
        'life_expectancy': float,
        'human_development_index': float,
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

    analysis_df = pd.read_csv(ppj("IN_DATA_OWID", "owid-covid-data.csv"), dtype=owid_dtypes, parse_dates=["date"])

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
        [analysis_df.date, analysis_df.iso_code],
        names=("date", "iso_code"),
    )
    analysis_df.index = pd.MultiIndex.from_arrays(
        [
            analysis_df.index.get_level_values(0).date,
            analysis_df.index.get_level_values(1),
        ]
    )

    analysis_df.loc[:, "new_cases_7d"] = analysis_df.new_cases.rolling(
        window=7, on=analysis_df.index.levels[0]
    ).sum()
    analysis_df.loc[
        analysis_df.groupby(axis=0, level=1).head(6).index, "new_cases_7d"
    ] = np.nan
    analysis_df.loc[:, "new_cases_14d"] = analysis_df.new_cases.rolling(
        window=14, on=analysis_df.index.levels[0]
    ).sum()
    analysis_df.loc[
        analysis_df.groupby(axis=0, level=1).head(13).index, "new_cases_14d"
    ] = np.nan
    analysis_df.loc[:, "new_cases_7d_per_100k"] = (
        analysis_df.new_cases_7d / analysis_df.population * 1e5
    )
    analysis_df.loc[:, "new_cases_14d_per_100k"] = (
        analysis_df.new_cases_14d / analysis_df.population * 1e5
    )

    countries = [
        "USA",
        "DEU",
        "FRA",
        "ITA",
        "ESP",
        "LBN",
        "JOR",
        "TUR",
        "IRQ",
        "SYR",
        "PAK",
        "AFG",
        "KEN",
        "ETH",
        "UGA",
        "COL",
        "PAK",
        "BRA",
    ]
    # countries = ["PAK"]

    for country in countries:
        country_data = analysis_df[analysis_df["iso_code"] == country]
        plot_development_over_time(country_data)
