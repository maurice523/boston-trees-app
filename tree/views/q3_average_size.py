import streamlit as st
import pandas as pd
import altair as alt


def load_data():
    df = pd.read_csv("tree/views/bprd_trees(in).csv")
    df["dbh"] = pd.to_numeric(df["dbh"], errors="coerce")
    df["neighborhood"] = df["neighborhood"].fillna("Unknown")
    return df


df = load_data()
st.title("Neighborhood")
st.write(
    "This page looks at tree size in each neighborhood. Tree size is measured "
    "using DBH (diameter at breast height, in inches). You can choose neighborhoods "
    "to compare, and see how their tree sizes differ."
)

df_valid = df.dropna(subset=["dbh"]).copy()
groups = df_valid.groupby("neighborhood")["dbh"]
mean_dbh = groups.mean()
count_trees = groups.count()

summary = pd.DataFrame({
    "Neighborhood": mean_dbh.index,
    "Average DBH (inches)": mean_dbh.values,
    "Tree count": count_trees.values
})

summary = summary.reset_index(drop=True)
summary.columns = ["Neighborhood", "Average DBH (inches)", "Tree count"]
summary_sorted = summary.sort_values(
    "Average DBH (inches)", ascending=False
)

neighborhoods_ordered = summary_sorted["Neighborhood"].tolist()

st.subheader("Compare tree size across neighborhoods")
default_selection = neighborhoods_ordered[:6]

################
selected_neighborhoods = st.multiselect(
    "Choose neighborhoods to compare:",
    options=neighborhoods_ordered,
    default=default_selection
)
################

if not selected_neighborhoods:
    st.info("Select at least one neighborhood to see the comparison.")
else:
    summary_selected = summary[
        summary["Neighborhood"].isin(selected_neighborhoods)
    ].copy()

    summary_selected = summary_selected.sort_values(
        "Average DBH (inches)", ascending=False
    )

    ordered_neighborhoods = summary_selected["Neighborhood"].tolist()

    st.subheader("Distribution of tree diameter at breast height (DBH)")

    st.write(
        "Each box shows the distribution of tree diameters in a neighborhood. "
        "The line inside the box is the median. The ends of the box show the "
        "middle 50% of tree sizes, and points outside are possible outliers."
    )

    df_selected = df_valid[df_valid["neighborhood"].isin(ordered_neighborhoods)]

    ################
    boxplot = (
        alt.Chart(df_selected)
        .mark_boxplot()
        .encode(
            x=alt.X(
                "neighborhood:N",
                sort=ordered_neighborhoods,
                title="Neighborhood"
            ),
            y=alt.Y(
                "dbh:Q",
                title="DBH (inches)"
            ),
            tooltip=["neighborhood", "dbh"]
        )
        .properties(height=400)
    )

    st.altair_chart(boxplot, use_container_width=True)

    st.subheader("Average tree size and tree count (selected neighborhoods)")

    summary_selected = summary_selected.reset_index(drop=True)
    summary_selected.index = summary_selected.index + 1

    st.dataframe(summary_selected, use_container_width=True)

    st.write(
        "The neighborhoods above are ranked from the largest average tree size "
        "to the smallest, based on the ones you selected. The boxplot uses the "
        "same order, so you can compare the full distribution of tree sizes."
    )
    ################
