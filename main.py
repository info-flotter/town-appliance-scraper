from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["POST"])
def scrape():
    data = request.json
    brand = data.get("brand")
    product_type = data.get("product_type")

    query_parts = []
    if brand:
        query_parts.append(brand)
    if product_type:
        query_parts.append(product_type)

    query = "+".join(query_parts) or "appliance"
    search_url = f"https://www.ajmadison.com/search.do?query={query}"
    res = requests.get(search_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    products = []
    cards = soup.select("div.product-tile-wrapper")

    for card in cards[:6]:
        name_el = card.select_one("div.product-title a")
        price_el = card.select_one("span.sales")
        was_el = card.select_one("span.was")

        if not name_el:
            continue

        name = name_el.get_text(strip=True)
        url = "https://www.ajmadison.com" + name_el.get('href')
        price = price_el.get_text(strip=True) if price_el else None
        was = was_el.get_text(strip=True) if was_el else None

        products.append({
            "product_name": name,
            "competitor_url": url,
            "price": price,
            "was_price": was,
        })

    return jsonify(products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
