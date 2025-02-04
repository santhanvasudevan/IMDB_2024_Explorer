#!pip install selenium
#!pip install webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
import time

# List of genres to scrape
genres_list = ["fantasy", "horror", "mystery",
              "romance", "sci-fi", "sport",
              "thriller"]  # Add more genres as needed

# Set up Edge WebDriver
options = webdriver.EdgeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

# Dictionary to store DataFrames
genre_dataframes = {}

for genre in genres_list:
    print(f"Scraping movies for genre: {genre}")

    # IMDb URL with dynamic genre
    url = f"https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres={genre}"
    driver.get(url)
    time.sleep(3)  # Allow page to load

    movie_list = []
    extracted_movies = 0
    prev_movie_count = 0

    while True:  # Loop until all movies are loaded
        try:
            # Get all movies currently loaded
            movies = driver.find_elements(By.CLASS_NAME, "sc-300a8231-0")

            # Ensure new movies are loaded before proceeding
            while len(movies) <= prev_movie_count:
                time.sleep(2)
                movies = driver.find_elements(By.CLASS_NAME, "sc-300a8231-0")

            for movie in movies[prev_movie_count:]:  # Process only new movies
                try:
                    title = movie.find_element(By.XPATH, './/h3[@class="ipc-title__text"]').text.strip()
                except:
                    title = "N/A"

                try:
                    release_year = movie.find_element(By.XPATH, './/span[contains(@class, "dli-title-metadata-item")]').text.strip()
                except:
                    release_year = "N/A"

                try:
                    duration = movie.find_element(By.XPATH, './/span[contains(@class, "dli-title-metadata-item")][2]').text.strip()
                except:
                    duration = "N/A"

                try:
                    rating = movie.find_element(By.XPATH, './/span[@class="ipc-rating-star--rating"]').text.strip()
                except:
                    rating = "N/A"

                try:
                    vote_count = movie.find_element(By.XPATH, './/span[@class="ipc-rating-star--voteCount"]').text.strip().replace("(", "").replace(")", "")
                except:
                    vote_count = "N/A"

                movie_list.append({
                    "Title": title,
                    "Year": release_year,
                    "Duration": duration,
                    "IMDb Rating": rating,
                    "Votes": vote_count
                })

                extracted_movies += 1

            prev_movie_count = len(movies)  # Update count after processing

            # Click "Load 50 more" button if available
            try:
                load_more_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "ipc-see-more__button")]'))
                )
                driver.execute_script("arguments[0].click();", load_more_button)
                print(f"Loaded more movies for {genre}... Extracted so far: {extracted_movies}")
                time.sleep(3)
            except:
                print(f"No more 'Load 50 more' button found for {genre}. Finished scraping.")
                break  # Exit loop if button not found

        except Exception as e:
            print(f"Error scraping {genre}: {e}")
            break

    # Convert to DataFrame and store in dictionary
    genre_dataframes[genre] = pd.DataFrame(movie_list)
    print(f"Scraped {len(movie_list)} movies for genre: {genre}")

    pd.DataFrame(movie_list).to_csv(f"IMDb_2024_{genre}_movies.csv", index=False)
    print(pd.DataFrame(movie_list).head())

# Close the driver
driver.quit()