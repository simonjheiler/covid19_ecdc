import os

import numpy as np
import pandas as pd

from bld.project_paths import project_paths_join as ppj
from src.utilities.data_utils import owid_dtypes

#####################################################
# PARAMETERS
#####################################################

idx = pd.IndexSlice


#####################################################
# FUNCTIONS
#####################################################


def _prepare_data_divi():

    file_list = os.listdir(ppj("IN_DATA", "divi"))
    files = [
        file
        for file in file_list
        if file.startswith("DIVI-Intensivregister_") and file.endswith(".csv")
    ]

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

    df = pd.DataFrame(columns=cols_analysis)

    for file in files:
        tmp_df = pd.read_csv(
            ppj("IN_DATA", "divi", file), dtype=float, parse_dates=["daten_stand"]
        )
        df = df.append(tmp_df)

    df = df.rename(
        columns={
            "daten_stand": "date",
            "faelle_covid_aktuell": "total_cases_hospitalized",
            "faelle_covid_aktuell_beatmet": "total_cases_ventilated",
            "betten_frei": "beds_vacant",
            "betten_belegt": "beds_occupied",
        }
    )

    df.date = df.date.dt.date
    df = df.groupby(["date"])[
        [
            "total_cases_hospitalized",
            "total_cases_ventilated",
            "beds_vacant",
            "beds_occupied",
        ]
    ].sum()

    # add variables
    df.loc[:, "ICU_covid_ventilated"] = df.total_cases_ventilated
    df.loc[:, "ICU_covid_not_ventilated"] = (
        df.total_cases_hospitalized - df.total_cases_ventilated
    )
    df.loc[:, "ICU_other"] = df.beds_occupied - df.total_cases_hospitalized
    df.loc[:, "ICU_vacant"] = df.beds_vacant
    df.loc[:, "ICU_capacity"] = df.beds_vacant + df.beds_occupied

    return df


def _prepare_data_owid():

    df = pd.read_csv(
        ppj("IN_DATA_OWID", "owid-covid-data.csv"),
        dtype=owid_dtypes,
        parse_dates=["date"],
    )

    # sort data
    df = df.sort_values(by=["iso_code", "date"])

    df.index = pd.MultiIndex.from_arrays(
        [df.date, df.iso_code], names=("date", "iso_code"),
    )
    df.index = pd.MultiIndex.from_arrays(
        [df.index.get_level_values(0).date, df.index.get_level_values(1)]
    )

    df.loc[idx[:, "DEU"], "new_tests"] = df.loc[idx[:, "DEU"], "total_tests"].diff(
        periods=7
    )

    df.loc[:, "new_cases_7d"] = df.new_cases.rolling(
        window=7, on=df.index.levels[0]
    ).sum()
    df.loc[df.groupby(axis=0, level=1).head(6).index, "new_cases_7d"] = np.nan

    df.loc[:, "new_cases_7d_per_100k"] = df.new_cases_7d / df.population * 1e5

    tmp_df = pd.merge(
        df.new_cases.groupby([df.date.dt.isocalendar().week, df.iso_code]).sum(
            min_count=1
        ),
        df.new_tests.groupby([df.date.dt.isocalendar().week, df.iso_code]).sum(
            min_count=1
        ),
        how="outer",
        left_index=True,
        right_index=True,
    )

    tmp_df = tmp_df.rename(
        columns={"new_cases": "new_cases_week", "new_tests": "new_tests_week"}
    )

    df = pd.merge(
        df,
        tmp_df,
        how="left",
        left_on=[df.date.dt.isocalendar().week.astype(str), df.iso_code.astype(str)],
        right_on=[
            tmp_df.index.get_level_values(0).astype(str),
            tmp_df.index.get_level_values(1).astype(str),
        ],
    )

    df.index = pd.MultiIndex.from_arrays(
        [df.date, df.iso_code], names=("date", "iso_code"),
    )
    df.index = pd.MultiIndex.from_arrays(
        [df.index.get_level_values(0).date, df.index.get_level_values(1)]
    )

    df.loc[:, "new_cases_week_per_100k"] = df.new_cases_week / df.population * 1e5

    df.loc[:, "new_tests_week_per_100k"] = df.new_tests_week / df.population * 1e5

    df.loc[:, "new_cases_14d"] = df.new_cases.rolling(
        window=14, on=df.index.levels[0]
    ).sum()
    df.loc[df.groupby(axis=0, level=1).head(13).index, "new_cases_14d"] = np.nan

    df.loc[:, "new_cases_14d_per_100k"] = df.new_cases_14d / df.population * 1e5

    df.loc[:, "new_tests_7d"] = df.new_tests.rolling(
        window=7, on=df.index.levels[0]
    ).sum()
    df.loc[df.groupby(axis=0, level=1).head(6).index, "new_tests_7d"] = np.nan

    df.loc[:, "new_tests_14d"] = df.new_tests.rolling(
        window=14, on=df.index.levels[0]
    ).sum()
    df.loc[df.groupby(axis=0, level=1).head(13).index, "new_tests_14d"] = np.nan

    df.loc[:, "new_tests_7d_per_100k"] = df.new_tests_7d / df.population * 1e5

    df.loc[:, "new_tests_14d_per_100k"] = df.new_tests_14d / df.population * 1e5

    df.loc[:, "positive_rate_7d"] = df.new_cases_7d / df.new_tests_7d

    df.loc[:, "positive_rate_14d"] = df.new_cases_14d / df.new_tests_14d

    df.loc[:, "positive_rate_week"] = df.new_cases_week / df.new_tests_week

    return df


#####################################################
# SCRIPT
#####################################################

if __name__ == "__main__":

    # get data
    divi_df = _prepare_data_divi()
    owid_df = _prepare_data_owid()

    # store formatted data sets
    divi_df.to_csv(ppj("OUT_DATA", "divi_data.csv"))
    owid_df.to_csv(ppj("OUT_DATA", "owid_data.csv"))
