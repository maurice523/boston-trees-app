import streamlit as st
import pandas as pd
import altair as alt
from views.data import load_trees


df = load_trees()

st.title("Relationship Between Rarity and Tree Size")

st.write(
    "This page looks at the relationship between **how rare a species is** "
    "and the **average size** of its trees.\n\n"
    "Use the slider to decide what counts as a **rare** species (based on "
    "the total number of trees of that species in the dataset). "
    "The scatterplot shows each species as a point."
)

species_counts = df["spp_com"].value_counts()
avg_dbh_per_species = (df.groupby("spp_com")["dbh"].mean())

summary = pd.DataFrame(
    {
    "Species": species_counts.index,
    "Total trees": species_counts.values,
    "Average DBH (inches)": avg_dbh_per_species.reindex(species_counts.index).values,
})

total_species = len(summary)

box_rarity = st.selectbox("Define 'rare' as species with less than these trees:", options=range(1,51))

rarity_threshold = st.slider(
    "",
    min_value=1,
    max_value=max(summary["Total trees"]),
    step=1,
    value= int(box_rarity),
)

################
summary["Rarity"] = summary["Total trees"].apply(
    lambda x: "Rare" if x <= rarity_threshold else "Common"
)
################

num_rare_species = (summary["Rarity"] == "Rare").sum()
percent_rare = num_rare_species / total_species * 100

col1, col2 = st.columns(2)
with col1:
    st.metric(
        "Number of rare species",
        f"{num_rare_species} / {total_species}"
    )
with col2:
    st.metric(
        "Percent of species that are rare",
        f"{percent_rare:.1f}%"
    )

st.subheader("Rarity vs average tree size")

st.write(
    "Each point represents one species. The x-axis shows the **average DBH** "
    "(tree diameter in inches) for that species. The y-axis shows how many "
    "trees of that species are in the dataset. Points in a different color "
    "are the species considered **rare** under your threshold."
)

################
scatter = (
    alt.Chart(summary)
    .mark_circle(size=80)
    .encode(
        x=alt.X(
            "Average DBH (inches):Q",
            title="Average DBH (inches)"
        ),
        y=alt.Y(
            "Total trees:Q",
            title="Total number of trees"
        ),
        color=alt.Color(
            "Rarity:N",
            scale=alt.Scale(domain=["Rare", "Common"],
                            range=["#e15759", "#4e79a7"]),
            legend=alt.Legend(title="Rarity (under current threshold)")
        ),
        tooltip=["Species", "Total trees", "Average DBH (inches)", "Rarity"],
    )
    .properties(height=400)
)

st.altair_chart(scatter, use_container_width=True)

st.write(
    "If most of the red points (rare species) are on the left, it means "
    "rare species tend to have smaller trees. If they are mostly on the right, "
    "rare species tend to have larger trees."
)

st.subheader("Species considered rare under this threshold")

rare_table = summary[summary["Rarity"] == "Rare"].copy()
rare_table = rare_table.sort_values("Total trees", ascending=False)
rare_table = rare_table.reset_index(drop=True)
rare_table.index = rare_table.index + 1

st.dataframe(rare_table, use_container_width=True)

st.write(
    "This table lists all species that are considered **rare** under your "
    f"selected threshold of **{rarity_threshold}** trees. It also shows their "
    "average tree size (DBH)."
)
