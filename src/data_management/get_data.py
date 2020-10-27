import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


#######################
# FUNCTIONS
#######################


def plot_development_over_time(input_data):

    # collect data
    plot_x = input_data["reporting_date"]
    plot_y = np.array(
        [
            input_data["cases_cumulative"].astype("Int64"),
            input_data["cases"].astype("Int64"),
            input_data["deaths_cumulative"].astype("Int64"),
            input_data["deaths"].astype("Int64"),
            input_data["cases_7d_100k"].astype("Float64"),
            input_data["cases_14d_100k"].astype("Float64"),
        ],
        dtype=np.float,
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

    url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    IN_DATA = "data/"

    file_name_data = "COVID-19-geographic-disbtribution-worldwide.csv"
    file_name_codes = "country_and_continent_codes.csv"

    # get data from server and store locally
    my_file = requests.get(url)
    open(IN_DATA + file_name_data, "wb").write(my_file.content)

    # load data into data frame
    analysis_df = pd.read_csv(IN_DATA + file_name_data)
    country_codes = pd.read_csv(IN_DATA + file_name_codes)

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

    # rename columns
    analysis_df = analysis_df.rename(
        columns={
            "dateRep": "reporting_date",
            "countriesAndTerritories": "country_name",
            "geoId": "country_code_short",
            "countryterritoryCode": "country_code",
            "popData2019": "population_size",
            "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000": "cases_14d_100k",
        }
    )

    # add continent names and codes
    analysis_df = pd.merge(
        analysis_df,
        country_codes[
            ["Continent_Name", "Continent_Code", "Three_Letter_Country_Code"]
        ],
        left_on="country_code",
        right_on="Three_Letter_Country_Code",
    )
    analysis_df = analysis_df.rename(
        columns={
            "Continent_Name": "continent_name",
            "Continent_Code": "continent_code",
        }
    )

    # properly format data types
    analysis_df["reporting_date"] = analysis_df["reporting_date"] = pd.to_datetime(
        analysis_df["reporting_date"], dayfirst=True
    )
    analysis_df["cases"] = analysis_df["cases"].astype("Int64")
    analysis_df["deaths"] = analysis_df["deaths"].astype("Int64")
    analysis_df["population_size"] = analysis_df["population_size"].astype("Int64")

    # sort data
    analysis_df = analysis_df.sort_values(by=["country_code", "reporting_date"])

    # cumulative sums for cases and deaths
    analysis_df["cases_cumulative"] = (
        analysis_df.groupby("country_code")["cases"].cumsum().astype("Int64")
    )
    analysis_df["deaths_cumulative"] = (
        analysis_df.groupby("country_code")["deaths"].cumsum().astype("Int64")
    )

    analysis_df.index = pd.MultiIndex.from_arrays(
        [analysis_df.reporting_date, analysis_df.country_code],
        names=("reporting_date", "country_code"),
    )
    analysis_df.index = pd.MultiIndex.from_arrays(
        [
            analysis_df.index.get_level_values(0).date.astype(str),
            analysis_df.index.get_level_values(1),
        ]
    )
    analysis_df.loc[:, "cases_7d"] = analysis_df.cases.rolling(
        window=7, on=analysis_df.index.levels[0]
    ).sum()
    analysis_df.loc[
        analysis_df.groupby(axis=0, level=1).head(6).index, "cases_7d"
    ] = np.nan
    analysis_df.loc[:, "cases_7d_100k"] = (
        analysis_df.cases_7d / analysis_df.population_size * 1e5
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
        country_data = analysis_df[analysis_df["country_code"] == country]
        plot_development_over_time(country_data)
