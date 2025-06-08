# RR_webscraper
WebScraper developed to extract information from the RunRepeat website


## About the files
- `main.py`: The main script that calls the web scraping functions.
- `getlinks.py`: The main script that contains the web scraping logic to gather links from the RunRepeat website.
- `getshoe.py`: The script that extracts detailed information about shoes from the links gathered by `getlinks.py`.
- `requirements.txt`: A file listing the required Python packages for the web scraper.
- `Processing.ipynb`: A notebook for some exploratory data analysis and cleaning on the scraped data.

## Usage
1. Install the required packages by running:
    ```bash
    pip install -r requirements.txt
    ```
2. Run the web scraper:
    ```bash
    python main.py
    ```
3. The script will gather links from the RunRepeat website and extract detailed information about each shoe.
4. The results will be saved in a CSV file named `data/raw/{shoe_name}.csv`.
5. You can perform exploratory data analysis using the `Processing.ipynb` notebook.
