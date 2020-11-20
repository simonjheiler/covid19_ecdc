import os

import pandas as pd

from bld.project_paths import project_paths_join as ppj


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

    df.to_csv(ppj("OUT_DATA", "divi_data.csv"))
