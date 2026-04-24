import streamlit as st
import pandas as pd
import altair as alt

# Parts between ################ were writen with the help of ChatGPT


def load_data():
    df = pd.read_csv("tree/views/bprd_trees(in).csv")

    df["neighborhood"] = df["neighborhood"].fillna("Unknown")
    df["spp_com"] = df["spp_com"].fillna("Unknown species")

    return df


# Load data for this page
df = load_data()

st.title("Most Common Tree Species in a Neighborhood")

st.write(
    "Choose a neighborhood. This page will show a pie chart and a table "
    "of the tree species found in that neighborhood."
)

neighborhoods = sorted(df["neighborhood"].unique().tolist())

selected_neighborhood = st.selectbox(
    "Select a neighborhood:",
    neighborhoods
)

################
condition = df["neighborhood"] == selected_neighborhood
################

filtered_df = df[condition]
df_nei = filtered_df.copy()


species_counts = df_nei["spp_com"].value_counts()

max_species = len(species_counts)

st.write(
    f"There are {max_species} different species in {selected_neighborhood}."
)

num_slices = st.slider(
    "Number of species to show in the pie chart:",
    min_value=2,
    max_value=max_species,
    value=min(15, max_species),   # default slider position = 15
    step=1,
)

# Top N species based on the slider (no cap here)
top_species = species_counts.head(num_slices)

# Group everything after the top N into "Other species"
other_count = species_counts.iloc[num_slices:].sum()


other_series = pd.Series({"Other species": other_count})
pie_data = pd.concat([top_species, other_series])

pie_df = pie_data.reset_index()
pie_df.columns = ["Species", "Tree count"]


species_list_neighborhood = species_counts.index.tolist()
top_15_neighborhood = species_list_neighborhood[0:15]

################
color_palette = [
    "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
    "#edc949", "#af7aa1", "#ff9da7", "#9c755f", "#bab0ab",
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"
]
################

species_color_map = {
"Other species": "#777777"
}

color_index = 0

for sp in species_list_neighborhood:
    species_color_map[sp] = color_palette[color_index]
    color_index = (color_index + 1) % len(color_palette)

legend_items = list(pie_df["Species"])

################
chart_domain = species_list_neighborhood + ["Other species"]
chart_range = [species_color_map[sp] for sp in chart_domain]

st.subheader(f"Species composition in {selected_neighborhood}")

pie_chart = (
    alt.Chart(pie_df)
    .mark_arc()
    .encode(
        theta=alt.Theta("Tree count:Q", title="Number of trees"),
        color=alt.Color(
            "Species:N",
            scale=alt.Scale(
                domain=chart_domain,
                range=chart_range,
            ),
            legend=alt.Legend(
                title="Species in this neighborhood",
                values=legend_items,   # legend shows only these entries
            ),
        ),
        tooltip=["Species", "Tree count"],
    )
)

st.altair_chart(pie_chart, use_container_width=True)

st.subheader(f"All species in {selected_neighborhood}")

species_table = species_counts.reset_index()
species_table.columns = ["Species", "Tree count"]
# Make the index start at 1
species_table.index = species_table.index + 1

st.dataframe(species_table, use_container_width=True)

st.write(
    "The pie chart changes based on how many species you select with the slider. "
    "The legend shows up to the 15 most common species in this neighborhood, "
    "plus 'Other species' if some species are grouped. The table lists every "
    "species in this neighborhood."
)
################