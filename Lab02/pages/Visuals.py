# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
with open("data.json", "r") as file:
    data = json.load(file)

# Convert JSON data to DataFrame
df = pd.DataFrame(data["data_points"])

# -----------------------------
# STATIC VISUALIZATION
# -----------------------------

st.header("Static Visualization")

st.write("Maximum Wind Speed by Hurricane")

st.bar_chart(
    df.set_index("name")["wind"]
)

# -----------------------------
# DYNAMIC VISUALIZATION
# -----------------------------

st.header("Dynamic Visualization")

if "selected_metric" not in st.session_state:
    st.session_state.selected_metric = "wind"

metric = st.radio(
    "Choose a statistic:",
    ["wind", "rainfall", "deaths"]
)

st.session_state.selected_metric = metric

fig = px.scatter(
    df,
    x="name",
    y=st.session_state.selected_metric,
    size=st.session_state.selected_metric,
    color="name",
    title=f"{st.session_state.selected_metric.capitalize()} by Hurricane"
)

fig.update_layout(
    xaxis_title="Hurricane",
    yaxis_title=st.session_state.selected_metric.capitalize()
)

current_mean = df[st.session_state.selected_metric].mean()
current_median = df[st.session_state.selected_metric].median()

if "previous_mean" not in st.session_state:
    st.session_state.previous_mean = current_mean

delta_mean = current_mean - st.session_state.previous_mean

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label=f"Mean {st.session_state.selected_metric.capitalize()}",
        value=round(current_mean, 2),
        delta=round(delta_mean, 2)
    )

with col2:
    st.metric(
        label=f"Median {st.session_state.selected_metric.capitalize()}",
        value=round(current_median, 2)
    )

st.session_state.previous_mean = current_mean

st.plotly_chart(fig)


# PART 2: GRAPHS FROM data.csv
st.divider()

st.title("CSV Visualizations")

# Read CSV data
csv_df = pd.read_csv("data.csv")

# -----------------------------
# STATIC VISUALIZATION
# -----------------------------

st.header("CSV Static Visualization")

category_counts = csv_df["Category"].value_counts()

st.bar_chart(category_counts)

# -----------------------------
# DYNAMIC VISUALIZATION
# -----------------------------

st.header("CSV Dynamic Visualization")

if "csv_chart_type" not in st.session_state:
    st.session_state.csv_chart_type = "Pie Chart"

chart_type = st.radio(
    "Choose a chart type:",
    ["Pie Chart", "Bar Chart"]
)

st.session_state.csv_chart_type = chart_type

if st.session_state.csv_chart_type == "Pie Chart":

    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title="Category Distribution"
    )

    st.plotly_chart(fig)

else:

    fig = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        title="Category Distribution"
    )

    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Count"
    )

    st.plotly_chart(fig)