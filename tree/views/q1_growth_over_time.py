import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Parts between ################ were writen with the help of ChatGPT


def load_data():
    df = pd.read_csv("tree/views/bprd_trees(in).csv")
    list_valid = df["date_plant"].notna() & (df["date_plant"] != "--")
    years = []
    num = 0
    for str_year in df["date_plant"]:
        if list_valid[num]:
            str_year = str_year.strip()
            list_year = str_year.split(" ")
            years.append(int(list_year[1]))
        num += 1
    df.loc[list_valid, "plant_year"] = years

    ################
    df["radius"] = df["dbh"].fillna(0) * 15.0 + 50.0
    ################
    return df


# Load the data for this page
df = load_data()

st.title("Growth of Boston's Tree Canopy Over Time ")
st.subheader("According to Boston Parks and Recreation Department (BPRD)")

st.write(
    "Use the slider to choose a year. The map will show all trees"
    "planted **up to** that year (based on the planting year "
    "recorded in the data)."
)

df_year_only = df.dropna(subset=["plant_year"]).copy()
min_year = int(df_year_only["plant_year"].min())
max_year = int(df_year_only["plant_year"].max())

selected_year = st.slider(
    "Show trees planted up to year:",
    min_value=min_year,
    max_value=max_year,
    step=1,
)

filtered = df_year_only[df_year_only["plant_year"] <= selected_year]
st.subheader(f"Trees planted up to {selected_year}")

################
col1, col2 = st.columns(2)
with col1:
    st.metric("Number of trees", f"{len(filtered):,}")
with col2:
    st.metric("Unique species", filtered["spp_com"].nunique())

view_state = pdk.ViewState(
    latitude=float(filtered["POINT_Y"].mean()),
    longitude=float(filtered["POINT_X"].mean()),
    zoom=11,
    pitch=0,
)

layer = pdk.Layer(
    "ScatterplotLayer",
    filtered,
    get_position="[POINT_X, POINT_Y]",
    get_radius="radius",
    get_fill_color="[0, 140, 0, 150]",
    pickable=True,
)

tooltip = {
    "text": (
        "Species: {spp_com}\n"
        "DBH (in): {dbh}\n"
        "Neighborhood: {neighborhood}\n"
        "Planting year: {plant_year}"
    ),
    "style": {
        "backgroundColor": "rgba(0, 0, 0, 0.8)",
        "color": "white",
    },
}

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
)

st.pydeck_chart(deck, use_container_width=True)

st.write(
    "As you move the slider to later years, more trees appear. "
    "This shows how the recorded tree canopy has grown over time "
    "in the dataset."
)
################