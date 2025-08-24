from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_product(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1')
        price = soup.find('div', class_='price')
        image = soup.find('img', class_='main-image')

        return {
            "url": url,
            "title": title.get_text(strip=True) if title else None,
            "price": price.get_text(strip=True) if price else None,
            "image": image['src'] if image and image.has_attr('src') else None
        }
    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    urls = data.get('urls', [])

    if not isinstance(urls, list):
        return jsonify({"error": "Invalid input. Expected 'urls' as a list."}), 400

    results = [scrape_product(url) for url in urls]
    return jsonify(results)

@app.route('/')
def home():
    return 'Scraper is running!'
