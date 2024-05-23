# scraping along with reviews 

import requests
from bs4 import BeautifulSoup

# Read the HTML file
file_path = 'webpage_amazon.html'
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all product titles, ratings, href links, and prices
product_info = []
product_titles = soup.find_all('span', class_='a-size-base-plus a-color-base a-text-normal')
product_links = []
product_prices = []

# Extract href links associated with product titles
for title in product_titles:
    parent_div = title.find_parent('div', class_='s-result-item')
    link = parent_div.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    if link:
        product_links.append("https://www.amazon.in" + link['href'])
    else:
        product_links.append('N/A')

# Extract price data associated with product titles
for title in product_titles:
    parent_div = title.find_parent('div', class_='s-result-item')
    price = parent_div.find('span', class_='a-offscreen')
    if price:
        product_prices.append(price.text.strip())
    else:
        product_prices.append('N/A')

# Extract rating data associated with product titles
for title in product_titles:
    parent_div = title.find_parent('div', class_='s-result-item')
    
    # Extract rating value
    rating_element = parent_div.find('span', class_='a-icon-alt')
    if rating_element:
        rating_text = rating_element.text.strip()
        rating_value = float(rating_text.split()[0])  # Extracting the first number from the rating text
    else:
        rating_value = 0.0  # Default rating if not found
    
    # Extract rating count
    rating_count_element = parent_div.find('span', class_='a-size-base s-underline-text')
    if rating_count_element:
        rating_count_text = rating_count_element.text.strip().replace(',', '')  # Remove commas from rating count
        rating_count = int(rating_count_text)
    else:
        rating_count = 0  # Default rating count if not found
    
    product_info.append((title.text.strip(), rating_value, rating_count))

# Sort the products based on ratings (highest to lowest) and rating count (highest to lowest)
product_info.sort(key=lambda x: (x[2], x[1]), reverse=True)  # Sort by rating count first, then by rating value

# Get the top 5 products with the highest ratings and rating count
top_5_products = product_info[:5]

# Function to get top 5 reviews from a product page
def get_top_reviews(product_url):
    response = requests.get(product_url, headers={"User-Agent": "Mozilla/5.0"})
    product_soup = BeautifulSoup(response.content, 'html.parser')
    reviews = []

    # Find review divs
    review_divs = product_soup.find_all('div', {'id': lambda x: x and x.startswith('customer_review-')}, limit=5)
    
    for review_div in review_divs:
        review_text = review_div.find('span', {'data-hook': 'review-body'}).text.strip()
        reviews.append(review_text)
    
    return reviews

# Print the top 5 product titles, prices, ratings, rating values, href links, and top 5 reviews
for i, (title, rating, rating_count) in enumerate(top_5_products, start=1):
    print(f"{i}. Title: {title}")
    print(f"   Price: {product_prices[i-1]}")
    print(f"   Rating: {rating}")
    print(f"   Rating Value: {rating_count}")
    print(f"   Href: {product_links[i-1]}")
    print(f"   Top 5 Reviews:")
    
    if product_links[i-1] != 'N/A':
        reviews = get_top_reviews(product_links[i-1])
        for j, review in enumerate(reviews, start=1):
            print(f"      {j}. {review}")
    else:
        print("      No reviews found.")
    print()
