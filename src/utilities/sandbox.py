import copy  # noqa:F401
import json  # noqa:F401
import multiprocessing  # noqa:F401
import os  # noqa:F401

import matplotlib.dates as mdates  # noqa:F401
import matplotlib.pyplot as plt  # noqa:F401
import numpy as np  # noqa:F401
import pandas as pd  # noqa:F401
from pandas.io.json import json_normalize  # noqa:F401
from scipy import interpolate  # noqa:F401

from bld.project_paths import project_paths_join as ppj  # noqa:F401

#####################################################
# PARAMETERS
#####################################################


#####################################################
# FUNCTIONS
#####################################################


#####################################################
# SCRIPT
#####################################################

if __name__ == "__main__":

    file_list = os.listdir(ppj("IN_DATA", "divi"))
    files = [
        file
        for file in file_list
        if file.startswith("DIVI-Intensivregister_") and file.endswith(".csv")
    ]

    # file_list = os.listdir(ppj("IN_DATA", "divi_json"))
    # files = [file for file in file_list if file.endswith("_intensivregister.json")]
    # for file in files:
    #     divi_df = json.load(open(ppj("IN_DATA", "divi_json", file)))

    cols_analysis = [
        "bundesland",
        "gemeindeschluessel",
        "anzahl_meldebereiche",
        "faelle_covid_aktuell",
        "faelle_covid_aktuell_beatmet",
        "anzahl_standorte",
        "betten_frei",
        "betten_belegt",
        "daten_stand",
    ]

    analysis_df = pd.DataFrame(columns=cols_analysis)

    for file in files:
        tmp_df = pd.read_csv(
            ppj("IN_DATA", "divi", file), dtype=float, parse_dates=["daten_stand"]
        )
        analysis_df = analysis_df.append(tmp_df)

    analysis_df = analysis_df.rename(
        columns={
            "daten_stand": "date",
            "faelle_covid_aktuell": "total_cases_hospitalized",
            "faelle_covid_aktuell_beatmet": "total_cases_ventilated",
            "betten_frei": "beds_vacant",
            "betten_belegt": "beds_occupied",
        }
    )

    analysis_df.date = analysis_df.date.dt.date
    df = analysis_df.groupby(["date"])[
        [
            "total_cases_hospitalized",
            "total_cases_ventilated",
            "beds_vacant",
            "beds_occupied",
        ]
    ].sum()

    df.to_csv(ppj("IN_DATA", "divi_data.csv"))

    # clean country codes
    country_codes = pd.read_csv(
        ppj("IN_DATA", "misc", "country_and_continent_codes.csv")
    )

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
