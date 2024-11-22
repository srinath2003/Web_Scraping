import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import time
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def fetch_amazon_data(product_name):
    def amazon_data(product_response):
        soup = BeautifulSoup(product_response.content, 'html.parser')

        # Extracting product names
        names = [tag.get_text().strip() for tag in soup.find_all("span", {"class": 'a-size-medium a-color-base a-text-normal'})]
        # Extracting prices
        prices = [tag.get_text().strip().replace(',', '') for tag in soup.find_all("span", {"class": 'a-price-whole'})]
        # Extracting ratings
        ratings = [tag.get_text().strip().replace('out of 5 stars', '') for tag in soup.find_all("span", {"class": 'a-icon-alt'})]

        # Extracting rating counts
        rating_counts = []
        for div in soup.find_all("div", {"class": "a-row a-size-small"}):
            rating_count_element = div.find("span", {"class": "a-size-base"})
            if rating_count_element:
                rating_counts.append(rating_count_element.get_text().strip().replace(',', ''))
            else:
                rating_counts.append('0')

        # Extracting original prices
        original_prices = []
        for span in soup.find_all("span", {"class": "a-price a-text-price"}):
            original_price_span = span.find("span", {"class": 'a-offscreen'})
            if original_price_span:
                original_prices.append(original_price_span.get_text().strip().replace('₹', '').replace(',', ''))
            else:
                original_prices.append(None)

        return names, prices, ratings, original_prices, rating_counts

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    session = requests.Session()

    retry = Retry(
        total=5,  # Increased retry count
        backoff_factor=2,  # Increased backoff factor (wait longer between retries)
        allowed_methods=["HEAD", "GET", "POST"],  # Updated to use allowed_methods
        status_forcelist=[500, 502, 503, 504],
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    base_url = 'https://www.amazon.in'
    url = f'https://www.amazon.in/s?k={product_name}'

    try:
        base_response = session.get(base_url, headers=headers)
        cookies = base_response.cookies
        product_response = session.get(url, headers=headers, cookies=cookies)

        if product_response.status_code == 200:
            names, prices, ratings, original_prices, rating_counts = amazon_data(product_response)

            # Normalize data lengths
            min_length = min(len(names), len(prices), len(ratings), len(original_prices), len(rating_counts))
            names = names[:min_length]
            prices = [int(price) for price in prices[:min_length]]
            ratings = ratings[:min_length]
            original_prices = [
                int(original_price) if original_price else None for original_price in original_prices[:min_length]
            ]
            rating_counts = rating_counts[:min_length]

            # Calculate discounts
            discounts = [
                int(round(((original_price - price) / original_price) * 100)) if original_price else None
                for original_price, price in zip(original_prices, prices)
            ]

            # Prepare DataFrame
            data = {
                'Name': names,
                'Price': prices,
                'Original_Price': original_prices,
                'Discount (%)': discounts,
                'Rating': ratings,
                'Rating_Count': rating_counts
            }

            df = pd.DataFrame(data)

            # Save as a unique CSV file
            folder = '/home/srinath2003/Desktop/amazon_extract_data'
            os.makedirs(folder, exist_ok=True)
            file_path = os.path.join(folder, f'{product_name}_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
            df.to_csv(file_path, index=False)
            print(f"Data saved to {file_path}")
        else:
            print(f"Failed to fetch Amazon data, status code: {product_response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    # Add a delay to avoid too many requests in a short period
    time.sleep(5)  # 5-second delay

if __name__ == "__main__":
    product_name = "laptop"  # You can change this to any product name you want to search for
    fetch_amazon_data(product_name)
