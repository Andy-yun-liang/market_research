# Shopify Scraper

## Overview
This project is designed to scrape eCommerce business data from various stores in my city, using an open data portal as a source for business URLs. The scraped product data is then stored in a **SQLite database** for further analysis.

## Features
- Reads eCommerce business URLs from an **open data portal CSV**.
- Scrapes **Shopify store data** via `/products.json` API.
- Stores structured product data into an **SQLite database**.
- Handles errors and logs failed requests.

## Tech Stack
- **Scrapy** – for web scraping
- **SQLite** – for data storage
- **Python (orjson, csv, logging, rich)** – for data handling and debugging

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Andy-yun-liang/market_research.git
   cd shopify-scraper
   ```
2. Create a virtual environment
   ```sh
   python -m venv venv
   source venv/bin/activate  
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Ensure you have a CSV file (`urls.csv`) with business URLs, structured like:
   ```csv
   https://shopifystore1.com
   https://shopifystore2.com
   https://shopifystore3.com
   ```
2. Run the Scrapy spider:
   ```sh
   scrapy crawl shopify_spider
   ```
3. The scraped data will be saved into an SQLite database (`data.db`).

## Project Structure
```
shopify_scraper/
│── spiders/
│   ├── shopify_spider.py  # The main Scrapy spider
│── data/
│   ├── urls.csv           # CSV with store URLs
│── db/
│   ├── raw_shopify_data.db            # SQLite database
│── requirements.txt       # Dependencies
│── README.md              # Project documentation
```

## Next Steps
- Improve error handling for non-Shopify stores.
- Start database normalization process so the data is useable
- Implement a dashboard for the various industries


