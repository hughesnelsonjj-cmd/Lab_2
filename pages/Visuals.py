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

if not os.path.exists("data.csv") or os.path.getsize("data.csv") == 0:
    st.warning("No survey data yet. Submit some responses on the Survey page first.")
    st.stop()

df = pd.read_csv("data.csv")

# ---------- STATIC: bar chart (Altair) ----------
st.subheader("Average Value by Category")
avg_df = df.groupby("category", as_index=False)["value"].mean()
bar = (
    alt.Chart(avg_df, title="Average Value by Category")
    .mark_bar()
    .encode(
        x=alt.X("category:N", title="Category"),
        y=alt.Y("value:Q", title="Average Value"),
        tooltip=["category", "value"],
    )
)
st.altair_chart(bar, use_container_width=True)

# ---------- DYNAMIC: pie chart with session state ----------
st.subheader("Share by Category (interactive)")

if "agg" not in st.session_state:
    st.session_state.agg = "sum"
if "selected_cats" not in st.session_state:
    st.session_state.selected_cats = sorted(df["category"].unique())

st.session_state.agg = st.radio(
    "Combine values using:", ["sum", "mean", "count"],
    index=["sum", "mean", "count"].index(st.session_state.agg),
    horizontal=True,
)
st.session_state.selected_cats = st.multiselect(
    "Categories to include:", sorted(df["category"].unique()),
    default=st.session_state.selected_cats,
)

filtered = df[df["category"].isin(st.session_state.selected_cats)]
if filtered.empty:
    st.info("Select at least one category.")
else:
    pie_df = (filtered.groupby("category")["value"]
              .agg(st.session_state.agg).reset_index(name="result"))
    pie = (
        alt.Chart(pie_df, title=f"{st.session_state.agg.title()} of Value by Category")
        .mark_arc()
        .encode(
            theta=alt.Theta("result:Q", title=st.session_state.agg.title()),
            color=alt.Color("category:N", title="Category"),
            tooltip=["category", "result"],
        )
    )
    st.altair_chart(pie, use_container_width=True)
