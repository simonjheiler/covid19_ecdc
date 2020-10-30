import copy  # noqa:F401
import json  # noqa:F401
import multiprocessing  # noqa:F401
import os  # noqa:F401

import matplotlib.dates as mdates  # noqa:F401
import matplotlib.pyplot as plt  # noqa:F401

import numpy as np  # noqa:F401
import pandas as pd  # noqa:F401

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
    files = [file for file in file_list if file.startswith("DIVI-Intensivregister_") and file.endswith(".csv")]

    cols_analysis = [
        "bundesland",
        "gemeindeschluessel",
        "anzahl_meldebereiche",
        "faelle_covid_aktuell",
        "faelle_covid_aktuell_beatmet",
        "anzahl_standorte",
        "betten_frei",
        "betten_belegt",
        "daten_stand"
    ]

    analysis_df = pd.DataFrame(columns=cols_analysis)

    for file in files:
        tmp_df = pd.read_csv(ppj("IN_DATA", "divi", file), dtype=float, parse_dates=["daten_stand"])
        analysis_df = analysis_df.append(tmp_df)

    analysis_df.daten_stand = analysis_df.daten_stand.dt.date
    df = analysis_df.groupby(["daten_stand"])[["faelle_covid_aktuell", "faelle_covid_aktuell_beatmet", "betten_frei", "betten_belegt"]].sum()

    df.rename(columns={"faelle_covid_aktuell": "total_cases_hospitalized", "faelle_covid_aktuell_beatmet": "total_cases_ventilated", "betten_frei": "beds_vacant", "betten_belegt": "beds_occupied"})

    print(analysis_df)


