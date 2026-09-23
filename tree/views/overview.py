import streamlit as st
import pandas as pd
import altair as alt
from views.data import load_trees


df = load_trees()

st.title("Overview of Boston Trees")

st.write("This program is a User-Interactive dashboard to show how Trees in Boston have been planted in the last serveral years. Enjoy!")

st.write(
    "This page shows a few charts to describe the tree data in Boston. "
    "The other pages will answer the four main questions of the project."
)

# ---------------------------------------------------------
# 1) Trees per neighborhood (top 15)
# ---------------------------------------------------------
st.subheader("Number of trees per neighborhood (top 15)")

neighborhood_counts = (
    df["neighborhood"]
    .fillna("Unknown")
    .value_counts()
    .reset_index()
)

neighborhood_counts.columns = ["Neighborhood", "Tree count"]
neighborhood_counts_top = neighborhood_counts.head(15)

chart_neighborhoods = (
    alt.Chart(neighborhood_counts_top)
    .mark_bar()
    .encode(
        x=alt.X("Tree count:Q", title="Number of trees"),
        y=alt.Y("Neighborhood:N", sort="-x", title="Neighborhood"),
        tooltip=["Neighborhood", "Tree count"],
        color=alt.value("#4c9f70")
    )
    .properties(height=400)
)

st.altair_chart(chart_neighborhoods, use_container_width=True)

# ---------------------------------------------------------
# 2) Top 10 species city-wide
# ---------------------------------------------------------
st.subheader("Top 10 most common tree species in Boston")

species_counts = (
    df["spp_com"]
    .fillna("Unknown species")
    .value_counts()
    .reset_index()
)

species_counts.columns = ["Species", "Tree count"]
species_counts_top = species_counts.head(10)

chart_species = (
    alt.Chart(species_counts_top)
    .mark_bar()
    .encode(
        x=alt.X("Species:N", sort="-y", title="Species (common name)"),
        y=alt.Y("Tree count:Q", title="Number of trees"),
        tooltip=["Species", "Tree count"],
        color=alt.value("#3b82f6")
    )
    .properties(height=400)
)

st.altair_chart(chart_species, use_container_width=True)

# ---------------------------------------------------------
# 3) Distribution of tree sizes (DBH)
# ---------------------------------------------------------
st.subheader("Distribution of tree diameter at breast height (DBH in inches)")

dbh_values = df["dbh"].dropna()
dbh_df = pd.DataFrame({"DBH": dbh_values})

chart_dbh = (
    alt.Chart(dbh_df)
    .mark_bar()
    .encode(
        x=alt.X("DBH:Q", bin=alt.Bin(maxbins=25), title="DBH (inches)"),
        y=alt.Y("count():Q", title="Number of trees"),
        tooltip=["count()"],
        color=alt.value("#f97316")
    )
    .properties(height=400)
)

st.altair_chart(chart_dbh, use_container_width=True)

st.write(
    "From these charts, you can see which neighborhoods have more trees, "
    "which species are most common overall, and whether most trees are "
    "small or large based on their diameter (DBH)."
)
