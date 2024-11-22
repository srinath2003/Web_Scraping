# Amazon Product Scraper

This is a Python script to scrape product details from Amazon India. The scraper fetches data such as product name, price, ratings, original price, and discount percentage, and saves the information in a CSV file.

## Features

- **Scrape Amazon India**: The script scrapes product data based on a given search term.
- **Product Details**: Fetches details such as:
  - Product name
  - Price
  - Original price
  - Discount percentage
  - Ratings and rating count
- **Save Data**: Data is saved to a CSV file with a timestamp for uniqueness.

## Requirements

Before running the script, ensure you have the following Python libraries installed:

- `requests`
- `beautifulsoup4`
- `pandas`
- `fake_useragent`
- `requests.adapters`

You can install the required libraries using the following command:

```bash
pip install requests beautifulsoup4 pandas fake_useragent
```
## How to Use

   Clone this repository to your local machine:
```
git clone https://github.com/srinath2003/Web_Scraping.git
```
Navigate to the project directory:
```
cd Web_Scraping/WebScraping_with_Airflow/
```
Open the amazon_scraper.py file and update the product_name variable with the product you want to search for.

product_name = "laptop"  # Change to the product you want to search for

Run the scraper:
```
    python amazon_scraper.py
```
   The script will scrape the data and save it as a CSV file in a folder named amazon_extract_data in your current directory.

Code Explanation

    Requests: The requests library is used to send HTTP requests to Amazon's product search page.
    BeautifulSoup: BeautifulSoup is used to parse the HTML response and extract product information.
    Pandas: The scraped data is organized into a Pandas DataFrame and saved as a CSV file.
    Retries and Delays: The script includes retry logic in case of failures (e.g., HTTP 503) and a delay to avoid overwhelming the server.

Troubleshooting

    HTTP 503 errors: Amazon may block requests if too many are sent in quick succession. The script includes retry logic and a delay between requests to help avoid this issue. If you still face errors, consider rotating your IP address using proxies.
    Missing product data: The script scrapes available product details, but Amazon’s product pages may vary. Some data (e.g., ratings or original prices) may not be available for all products.

License


This project is licensed under the MIT License - see the LICENSE file for details.
Author
