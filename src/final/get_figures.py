import json

import pandas as pd

from bld.project_paths import project_paths_join as ppj
from src.utilities.data_utils import owid_dtypes
from src.utilities.plot_utils import _plot_development_over_time
from src.utilities.plot_utils import _plot_stacked_area_100

#######################
# FUNCTIONS
#######################


#######################
# SCRIPT
#######################

if __name__ == "__main__":

    idx = pd.IndexSlice

    # load specs
    analysis_specs = json.load(open(ppj("IN_SPECS", "analysis_specs.json")))
    countries = analysis_specs["countries"]

    # load data
    owid_df = pd.read_csv(
        ppj("OUT_DATA", "owid_data.csv"), dtype=owid_dtypes, parse_dates=["date"],
    )
    owid_df.index = owid_df.date
    divi_df = pd.read_csv(
        ppj("OUT_DATA", "divi_data.csv"), parse_dates=["date"], dtype=float
    )
    divi_df.index = divi_df.date

    # plot divi data
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

    # plot owid data
    for country in countries:
        plot_data = owid_df[owid_df["iso_code"] == country]
        plot_params = {
            "title": f"Cases and tests ({country})",
            "outpath": ppj("OUT_FIGURES", "covid_time_series_" + country + ".pdf"),
        }
        _plot_development_over_time(plot_data, plot_params)
