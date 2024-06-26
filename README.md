# Estate Scraper

This project is a web scraper built using Scrapy and Playwright frameworks to extract real estate data from following real estate resources:

- https://kelm-immobilien.de/immobilien/
- https://www.adentz.de/wohnung-mieten-rostock/#/list1

Each spider extracts property details such as title, status, rent price, description, phone number, and email address. The extracted data is then stored or processed based on specific requirements.

## Installation

**Clone the repository:**

  ```
  git clone https://github.com/YevheniiNiestierov/Estate-Scrapper.git
  ```
  ```
  cd Estate-Scrapper
  ```
**Install requirements:**
  ```
  pip install -r requirements.txt
  ```

## Run it

  ```
  cd estate_scraper
  ```

**Spider for the first resource:**
  ```
  scrapy crawl respider -o output/germany/kelm-immobilien/estate_data.json
  ```

**For the second one**
  ```
  scrapy crawl adentz_spider -o output/germany/adentz/estate_data.json
  ```



