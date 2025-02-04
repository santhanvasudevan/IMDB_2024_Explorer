# IMDb 2024 Movies Explorer

## Overview
IMDb 2024 Movies Explorer is a Streamlit-based web application that allows users to explore, filter, and visualize IMDb movies data for 2024. The application reads movie data from CSV files, processes the data, and provides interactive visualizations and filtering options.

## Features
- **Load & Clean Data**: Reads movie data from multiple CSV files and cleans the data.
- **Filtering Options**: Users can filter movies based on runtime, vote count, IMDb rating, and genre.
- **Data Visualization**: Displays bar charts, histograms, pie charts, treemaps, and heatmaps to analyze the movie dataset.
- **Database Storage**: Saves the cleaned dataset into an SQLite database for further analysis.
- **Interactive UI**: Uses Streamlit's intuitive layout for easy data exploration.

## Installation
### Prerequisites
Ensure you have Python installed along with the required libraries. Install dependencies using the following command:

```sh
pip install streamlit pandas matplotlib seaborn squarify sqlite3
```

## Usage
1. **Prepare CSV Data**: Place all relevant CSV files in the project directory.
2. **Run the Application**:
   ```sh
   streamlit run IMDBExplorerapp.py
   ```
3. **Interact with Filters**: Select various filters for runtime, vote counts, IMDb ratings, and genres.
4. **Explore Data Visualizations**: Gain insights through various charts and tables which gets dynamically updated based on filters.

## Data Processing
- **Combining CSV Files**: The app reads all CSV files in the directory and merges them into a single DataFrame.
- **Data Cleaning**:
  - Extracts genre information from filenames.
  - Cleans movie titles by removing unnecessary numbers at the begining.
  - Converts runtime from `hh:mm` format to total minutes.
  - Converts vote counts from shorthand (e.g., `12K` to `12000`).
  - Handles missing IMDb ratings by imputing mean values.
- **Database Storage**:
  - Saves the cleaned dataset into an SQLite database (`database.sqlite`).
  - Verifies the data is stored correctly by reloading and displaying it.

## Application UI
### Filters Section
- **Runtime**: Filter movies by duration (Less than 2h, Between 2-3h, Over 3h).
- **Vote Count**: Filter based on popularity.
- **IMDb Rating**: Select movies with ratings above 6, 7, or 8.
- **Genre Selection**: Choose one or more genres.

### Data Display Section
- **Filtered Movie Table**: Displays a list of movies meeting selected criteria.
- **Interactive Charts**:
  - Genre distribution
  - Average runtime by genre
  - IMDb rating distribution
  - Voting trends by genre
  - Correlation analysis between rating and vote counts
  - Treemap for most popular movies per genre
  - Heatmap of IMDb ratings by genre

## Screenshots


## License
This project is open-source under the MIT License.

---

### Author
Santhan Vasudevan

