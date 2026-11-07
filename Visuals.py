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

df = pd.read_csv("data.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()   # remove stray spaces only; keeps capitalization

if not {"Category", "Value"}.issubset(df.columns):
    st.error(f"data.csv must have 'Category' and 'Value' columns, but found: {list(df.columns)}")
    st.stop()

df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
df = df.dropna(subset=["Category", "Value"])

# ---------- STATIC: bar chart (Altair) ----------
st.subheader("Average Value by Category")
avg_df = df.groupby("Category", as_index=False)["Value"].mean()
bar = (
    alt.Chart(avg_df, title="Average Value by Category")
    .mark_bar()
    .encode(
        x=alt.X("Category:N", title="Category"),
        y=alt.Y("Value:Q", title="Average Value"),
        tooltip=["Category", "Value"],
    )
)
st.altair_chart(bar, use_container_width=True)

# ---------- DYNAMIC: pie chart with session state ----------
st.subheader("Share by Category (interactive)")

if "agg" not in st.session_state:
    st.session_state.agg = "sum"
if "selected_cats" not in st.session_state:
    st.session_state.selected_cats = sorted(df["Category"].unique())

st.session_state.agg = st.radio(
    "Combine values using:", ["sum", "mean", "count"],
    index=["sum", "mean", "count"].index(st.session_state.agg),
    horizontal=True,
)
st.session_state.selected_cats = st.multiselect(
    "Categories to include:", sorted(df["Category"].unique()),
    default=st.session_state.selected_cats,
)

filtered = df[df["Category"].isin(st.session_state.selected_cats)]
if filtered.empty:
    st.info("Select at least one category.")
else:
    pie_df = (filtered.groupby("Category")["Value"]
              .agg(st.session_state.agg).reset_index(name="Result"))
    pie = (
        alt.Chart(pie_df, title=f"{st.session_state.agg.title()} of Value by Category")
        .mark_arc()
        .encode(
            theta=alt.Theta("Result:Q", title=st.session_state.agg.title()),
            color=alt.Color("Category:N", title="Category"),
            tooltip=["Category", "Result"],
        )
    )
    st.altair_chart(pie, use_container_width=True)
