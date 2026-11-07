# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import altair as alt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")

# READ JSON FILE

with open("data.json", "r") as file:
    data = json.load(file)

games = data["data_points"]
df = pd.DataFrame(games) 

# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---

st.title("Games Data Explorer")
st.header("Average rating by genre")

average_ratings = df.groupby("genre")["ratings"].mean()

fig, ax = plt.subplots()

average_ratings.plot(kind = "bar", ax = ax)

ax.set_title("Average Game Rating by Genre")
ax.set_xlabel("Genre")
ax.set_ylabel("Average Rating")

st.pyplot(fig)

st.header("Explore Games By Genre")

genres = sorted(df["genre"].unique())

if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = genres[0]

st.selectbox(
    "Choose a genre:",
    genres,
    key = "selected_genre"
    )

selected_genre = st.session_state.selected_genre
filtered_df = df[df["genre"] == selected_genre]
fig2, ax2 = plt.subplots()

ax2.scatter(
    filtered_df["title"],
    filtered_df["ratings"]
    )
ax2.set_title(f"Rating for {selected_genre} Games")
ax2.set_xlabel("Game")
ax2.set_ylabel("Rating")

plt.xticks(rotation = 45)
fig2.tight_layout()

st.pyplot(fig2)
plt.close(fig2) 

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---

st.header("Survey Data Analysis")

CSV_FILE = "data.csv"
if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
    st.warning("No survey data yet. Fill out the Survey page first.")
    st.stop()

df = pd.read_csv(CSV_FILE)

# ---------- STATIC: bar chart (Altair, advanced) ----------
st.subheader("Average Sleep by Class Year")
avg_sleep = df.groupby("year", as_index=False)["sleep_hours"].mean()
static_chart = (
    alt.Chart(avg_sleep, title="Average Nightly Sleep by Class Year")
    .mark_bar()
    .encode(
        x=alt.X("year:N", title="Class Year",
                sort=["Freshman", "Sophomore", "Junior", "Senior"]),
        y=alt.Y("sleep_hours:Q", title="Average Sleep (hours)"),
        tooltip=["year", "sleep_hours"],
    )
)
st.altair_chart(static_chart, use_container_width=True)

# ---------- DYNAMIC: scatter plot with session state ----------
st.subheader("Explore Relationships")

if "x_var" not in st.session_state:
    st.session_state.x_var = "sleep_hours"
if "y_var" not in st.session_state:
    st.session_state.y_var = "study_hours"
if "years" not in st.session_state:
    st.session_state.years = sorted(df["year"].unique())

options = ["sleep_hours", "study_hours", "caffeine_cups"]

st.session_state.x_var = st.selectbox(
    "X-axis", options, index=options.index(st.session_state.x_var)
)
st.session_state.y_var = st.selectbox(
    "Y-axis", options, index=options.index(st.session_state.y_var)
)
st.session_state.years = st.multiselect(
    "Class years to include",
    sorted(df["year"].unique()),
    default=st.session_state.years,
)

filtered = df[df["year"].isin(st.session_state.years)]

if filtered.empty:
    st.info("Select at least one class year.")
else:
    dynamic_chart = (
        alt.Chart(filtered, title=f"{st.session_state.y_var} vs. {st.session_state.x_var}")
        .mark_circle(size=100)
        .encode(
            x=alt.X(f"{st.session_state.x_var}:Q", title=st.session_state.x_var.replace("_", " ").title()),
            y=alt.Y(f"{st.session_state.y_var}:Q", title=st.session_state.y_var.replace("_", " ").title()),
            color=alt.Color("year:N", title="Class Year"),
            tooltip=["name", "year", "sleep_hours", "study_hours", "caffeine_cups"],
        )
    )
    st.altair_chart(dynamic_chart, use_container_width=True)
