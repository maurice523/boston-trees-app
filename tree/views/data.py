"""Shared tree data loading.

All five pages use this one cached loader, so the CSV is read and cleaned once
per session instead of once per page. Keeping it here also means the file path
lives in a single place.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# Next to this file, so it works no matter which folder the app is started from
CSV_PATH = Path(__file__).with_name("trees.csv")


@st.cache_data
def load_trees() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)

    # DBH (tree diameter) should be a number
    df["dbh"] = pd.to_numeric(df["dbh"], errors="coerce")

    # Fill in the blanks so grouping and filtering don't drop rows
    df["neighborhood"] = df["neighborhood"].fillna("Unknown")
    df["spp_com"] = df["spp_com"].fillna("Unknown species")

    # "Fall 2020" -> 2020; "--" and blanks become NaN
    df["plant_year"] = pd.to_numeric(
        df["date_plant"].astype(str).str.extract(r"(\d{4})")[0], errors="coerce"
    )

    # Circle size for the map: bigger trees draw bigger dots
    df["radius"] = df["dbh"].fillna(0) * 15.0 + 50.0

    return df
