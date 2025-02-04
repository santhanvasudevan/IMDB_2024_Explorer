# IMDb Data Scraping and Streamlit App
This repository contains two main functionalities:

**IMDb Data Scraping:** The first part of the project scrapes IMDb data based on selected genres, and stores the scraped information in CSV files.

**Streamlit Data Analysis App:** The second part of the project is a Streamlit app that reads the CSV data, cleans it, and provides multi-filter functionality and dynamic visualizations for user insights.

## Project Overview

**Step 1:** Scraping IMDb Data and Saving as CSV
The scraper collects data about movies from IMDb, based on a list of predefined genres. It uses the Selenium web scraping library and stores the data in CSV format, which includes columns like Title, Runtime, Genre, IMDb Rating, and Vote Counts. 

- The genres scraped include:
   - Fantasy
   - Horror
   - Mystery
   - Romance
   - Sci-Fi
   - Sport
   - Thriller

## Requirements:

- Python 3.x
- Selenium
- WebDriver Manager
- Pandas

## How to Run:

Install the required libraries using pip install(all given requirements).
Run the scraper script to collect and store the IMDb data in CSV files.
For detailed instructions on scraping, refer to the scraping_readme.md.

# Step 2: Streamlit App for Data Visualization
The Streamlit app reads the CSV files generated in the previous step. It allows users to interact with the data, apply multiple filters (genre, runtime, etc.), and visualize insights dynamically. 

The app includes features such as:

Interactive filters for genres, runtime, and more
Dynamic visualizations like bar charts and scatter plots, treemap
Displays top movies by rating and vote count
Shows genre distribution, average duration by genre, and voting trends

## Requirements:

- Streamlit
- Pandas
- Matplotlib
- Seaborn
- Squarify (for Treemaps)

## How to Run:

Install the required libraries using pip install (all given requirements).
Run the Streamlit app using 
  ```sh
  streamlit run app.py
  ```
For detailed instructions on creating and running the app, refer to the streamlit_readme.md.

## Getting Started
### To run the entire project:

Clone this repository.
Follow the instructions in the scraping_readme.md to scrape data from IMDb.
After scraping, run the streamlit_readme.md for instructions on setting up and running the Streamlit app.
