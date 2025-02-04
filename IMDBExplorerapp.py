import streamlit as st
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
import squarify  # For Treemap visualization
import sqlite3

# Get a list of all CSV files in the current directory using os
csv_files = [file for file in os.listdir() if file.endswith(".csv")]

dfmaster = pd.DataFrame()

for file in csv_files:
    df1 = pd.read_csv(file)
    df1["Genre"] = re.findall(r"2024_.*?\.",file)[0][5:-8]
    df1["Title"] = df1["Title"].str.replace(r"^\d{1,5}\. ", "", regex=True)
    dfmaster = pd.concat([dfmaster,df1], ignore_index=True)

def convert_runtime(runtime_str):
    if not isinstance(runtime_str, str):  # Ensure input is a string
        return None  # Or return a default value like 0
    match = re.match(r"(?:(\d+)h)?\s?(?:(\d+)m)?", runtime_str)
    if not match:  # If regex fails to match
        return None  # Or return a default value like 0
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    return hours * 60 + minutes  # Convert to total minutes


# Apply conversion
dfmaster["Runtime"] = dfmaster["Duration"].apply(convert_runtime)

def convert_votes(value):
    if pd.isna(value):  # Check for NaN and impute Zero
        return 0
    if isinstance(value, str) and "K" in value:
        return int(float(value.replace("K", "")) * 1000)
    try:
        return int(value)
    except ValueError:
        return 0  # Default for unexpected values


# Apply function and store in a new column
dfmaster["Vote Counts"] = dfmaster["Votes"].apply(convert_votes)

# Imputing mean value where rating is not available (rounded to 1 decimal place)
dfmaster['IMDb Rating'] = dfmaster['IMDb Rating'].fillna(dfmaster['IMDb Rating'].mean()).round(1)

# Imputing mean value where Duration is not available (rounded to no decimal places)
dfmaster['Runtime'] = dfmaster['Runtime'].fillna(dfmaster['Runtime'].mean()).round(0).astype(int)

# Copy to another df
# dfMoviesVis contains movies where genres are not combined
# dfmaster will contain only unique movies as genres will be combined
dfMoviesVis = dfmaster.copy()

# Drop unnecessary columns. Already cleaned and created new columns for these two data
dfmaster = dfmaster.drop(columns=['Votes', 'Duration']) 

# Group by 'Title', keeping max IMDb Rating and Vote Counts, and concatenating Genre
dfmaster = dfmaster.groupby(['Title', 'Year', 'Runtime']).agg(
    {'Genre': lambda x: ', '.join(set(x)), 'IMDb Rating': 'max', 'Vote Counts': 'max'}
).reset_index()

# Optionally save the dataframe to SQL database file
#---------------------------------------------------------------------------
# Create a connection to an SQLite database file
db_filename = "database.sqlite"  # SQL file
conn = sqlite3.connect(db_filename)

# Write the dataframe to a new table in the SQLite database
dfmaster.to_sql("users", conn, if_exists="replace", index=False)

# Close the connection
conn.close()
print(f"Database file '{db_filename}' created successfully.")
#----------------------------------------------------------------------------
# Check if data is saved correctly
conn = sqlite3.connect("database.sqlite")
df_check = pd.read_sql("SELECT * FROM users", conn)
conn.close()
print(df_check)
#----------------------------------------------------------------------------

# Create layout with three columns
st.set_page_config(layout="wide")
st.title("🎬 IMDb 2024 Movies Explorer")

#Setting layout 1:4:1 for filters in left and right and table in the center
col1, col2, col3 = st.columns([1, 4, 2])  # Left & right column for filters,  center column for table

# 🎛️ **LEFT COLUMN: Filters**
with col1:
    st.subheader("🎚️ Filters")

    # ⏳ **Runtime Filter**
    runtime_filter = st.radio("Select Runtime", ["All", "Less than 2h", "Between 2-3h", "Over 3h"])
    if runtime_filter == "Less than 2h":
        dfmaster = dfmaster[dfmaster["Runtime"] < 120]
        dfMoviesVis = dfMoviesVis[dfMoviesVis["Runtime"] < 120]
    elif runtime_filter == "Between 2-3h":
        dfmaster = dfmaster[(dfmaster["Runtime"] >= 120) & (dfmaster["Runtime"] <= 180)]
        dfMoviesVis = dfMoviesVis[(dfMoviesVis["Runtime"] >= 120) & (dfMoviesVis["Runtime"] <= 180)]

    elif runtime_filter == "Over 3h":
        dfmaster = dfmaster[dfmaster["Runtime"] > 180]
        dfMoviesVis = dfMoviesVis[dfMoviesVis["Runtime"] > 180]

    # 🔢 **Vote Count Filter**
    vote_filter = st.radio("Filter by Vote Count", ["All", "Over 1000", "Over 5000", "Over 10000"])
    if vote_filter == "Over 1000":
        dfmaster = dfmaster[dfmaster["Vote Counts"] > 1000]
        dfMoviesVis = dfMoviesVis[dfMoviesVis["Vote Counts"] > 1000]
    elif vote_filter == "Over 5000":
        dfmaster = dfmaster[dfmaster["Vote Counts"] > 5000]
        dfMoviesVis = dfMoviesVis[dfMoviesVis["Vote Counts"] > 5000]
    elif vote_filter == "Over 10000":
        dfmaster = dfmaster[dfmaster["Vote Counts"] > 10000]
        dfMoviesVis = dfMoviesVis[dfMoviesVis["Vote Counts"] > 10000]

    # ⭐ **IMDb Rating Filter**
    rating_filter = st.radio("Filter by IMDb Rating", ["All", "6+", "7+", "8+"])
    if rating_filter == "6+":
        dfmaster = dfmaster[dfmaster["IMDb Rating"] >= 6]
        dfMoviesVis = dfMoviesVis[dfMoviesVis["IMDb Rating"] >= 6]
    elif rating_filter == "7+":
        dfmaster = dfmaster[dfmaster["IMDb Rating"] >= 7]
        dfMoviesVis = dfMoviesVis[dfMoviesVis["IMDb Rating"] >= 7]
    elif rating_filter == "8+":
        dfmaster = dfmaster[dfmaster["IMDb Rating"] >= 8]
        dfMoviesVis = dfMoviesVis[dfMoviesVis["IMDb Rating"] >= 8]

# 🎭 **Genre Filter**
with col3:
    st.subheader("🎭 Genre selection Pane")
    all_genres = sorted(set(genre for sublist in dfmaster["Genre"].str.split(", ") for genre in sublist))
    selected_genres = st.multiselect("Select Genres", all_genres, default=all_genres)
    dfmaster = dfmaster[dfmaster["Genre"].apply(lambda x: any(genre in x for genre in selected_genres))]
    dfMoviesVis = dfMoviesVis[dfMoviesVis["Genre"].apply(lambda x: any(genre in x for genre in selected_genres))]

# 📊 **Center COLUMN: Display Filtered Movies**
with col2:
    st.subheader("📋 Filtered Movies")
    st.write(f"Showing {len(dfmaster)} movies:")
    st.dataframe(dfmaster[["Title", "Runtime", "Genre", "IMDb Rating", "Vote Counts"]], hide_index=True)


# 📊 **Data Visualizations using Subplots**
st.subheader("📊 Data Visualizations")
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14, 16))

# Genre Distribution
sns.barplot(x=dfMoviesVis["Genre"].value_counts().index, y=dfMoviesVis["Genre"].value_counts().values, ax=axes[0, 0], palette= "Spectral")
axes[0, 0].set_title("Genre Distribution")
axes[0, 0].set_ylabel("Movies Count")
axes[0, 0].tick_params(axis='x', rotation=90)

# Average Duration by Genre
df_expanded = dfMoviesVis.explode("Genre")
avg_duration = df_expanded.groupby("Genre")["Runtime"].mean()
sns.barplot(x=avg_duration.index, y=avg_duration.values, ax=axes[0, 1], palette= "coolwarm")
axes[0, 1].set_title("Average Duration by Genre")
axes[0, 1].set_ylabel("")
axes[0, 1].tick_params(axis='x', rotation=90)

# Voting Trends by Genre
avg_votes = df_expanded.groupby("Genre")["Vote Counts"].mean()
sns.barplot(x=avg_votes.index, y=avg_votes.values, ax=axes[1, 0], palette= "deep")
axes[1, 0].set_title("Voting Trends by Genre")
axes[1, 0].set_ylabel("Average Vote counts")
axes[1, 0].tick_params(axis='x', rotation=90)

# Rating Distribution
sns.histplot(dfMoviesVis["IMDb Rating"], kde=True, bins=10, ax=axes[1, 1], color="royalblue")
axes[1, 1].set_title("Rating Distribution")

# Most Popular Genres by Voting
genre_votes = dfMoviesVis.groupby("Genre")["Vote Counts"].sum()
genre_votes.plot.pie(
    autopct=lambda p: f'{p:.1f}%' if p > 5 else '',  # Hide small labels
    ax=axes[2, 0],
    cmap="viridis",
    colors=sns.color_palette("viridis", len(genre_votes)),
    startangle=140,  # Better alignment
    wedgeprops={'edgecolor': 'black', 'linewidth': 1}  # Add separation
)
axes[2, 0].set_title("Most Popular Genres by Voting")
axes[2, 0].set_ylabel("")

# Top movies in each genre using Treemap
top_movies = dfMoviesVis.loc[dfMoviesVis.groupby("Genre")["Vote Counts"].idxmax()]
labels = [f"{title}\n({genre})" for title, genre in zip(top_movies["Title"], top_movies["Genre"])]
squarify.plot(sizes=top_movies["Vote Counts"], label=labels, alpha=0.7, color=sns.color_palette("pastel"), ax=axes[2, 1])
axes[2, 1].set_title("Top Movies in Each Genre (Based on Most Votes)")
axes[2, 1].axis("off")

# Ratings by Genre Heatmap
rating_pivot = df_expanded.pivot_table(index="Genre", values="IMDb Rating", aggfunc="mean")
sns.heatmap(rating_pivot, annot=True, cmap="coolwarm", ax=axes[3, 0])
axes[3, 0].set_title("Ratings by Genre Heatmap")

# Correlation Analysis
sns.scatterplot(x=dfmaster["IMDb Rating"], y=dfmaster["Vote Counts"], ax=axes[3, 1])
axes[3, 1].set_title("Correlation Analysis: Ratings vs. Voting Counts")

plt.tight_layout()
st.pyplot(fig)