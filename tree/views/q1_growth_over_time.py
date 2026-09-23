import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from views.data import load_trees

# Parts between ################ were writen with the help of ChatGPT


df = load_trees()

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