from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime
from dataclasses import dataclass, field
import re
import logging

def write_json(data):
    with open("prices.json", 'w') as file:
        json.dump(data, file, indent=4)

def read_json() -> None:
    try:
        with open("prices.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

@dataclass
class Product:
    name: str
    prices: dict = field(default_factory=dict)

    def add_price(self, site, price: float) -> None:
        self.prices[site] = price

    def cheapest_site(self):
        if not self.prices:
            return None
        return min(self.prices, key=self.prices.get)

    def cheapest_price(self):
        return self.prices[self.cheapest_site()]

    def to_dict(self):
        return {
            "Date": datetime.now().isoformat(),
            "Name": self.name,
            "Prices": self.prices,
            "Cheapest Site": self.cheapest_site(),
            "Cheapest Price": self.cheapest_price()
        }

class WebsiteScraper:
    def __init__(self, site_name, url, css_selector):
        self.site_name = site_name
        self.url = url
        self.css_selector = css_selector

    def get_price(self, driver):
        driver.get(self.url)
        wait = WebDriverWait(driver, 10)
        item_price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.css_selector)))
        price_text = item_price.text
        match = re.search(r"\d+(\.\d+)?", price_text)
        if match:
            return float(match.group())
        else:
            raise ValueError("Price not found")

class PriceComparer:
    def __init__(self, product):
        self.product = product

    def compare(self):
        for site, price in self.product.prices.items():
            print(f"{site}: ${price}")
        print("\nCheapest Site: ", self.product.cheapest_site())
        print("\nCheapest Price: $", self.product.cheapest_price())


options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--headless=new")
driver = webdriver.Edge(options=options)

pokemon_box = Product ("Pokemon TCG: Scarlet & Violet: Prismatic Elite Box")
websites = [
    WebsiteScraper(
        "Walmart",
        "https://www.walmart.com/ip/13816151308",
        '[itemprop="price"]'
    ),
    WebsiteScraper(
        "Target",
        "https://www.target.com/p/pokemon-tcg-scarlet-violet-elite-trainer-box-prismatic-evolutions-of-the-pokemon-tcg-1-fully-illustrated-promo-card-9-booster-packs-premium/-/A-1008746912#lnk=sametab",
        '[data-test="product-price"]'
    )
]
def main():
    try:
        for site in websites:
            try:
                price = site.get_price(driver)
                pokemon_box.add_price(site.site_name, price)
                print(f"{site.site_name}: ${price}")
            except Exception as e:
                logging.error(f"There's been an error in scraping from {site.site_name}: {e}... sorry")
            for attempt in range(3):
                try:
                    return site.get_price(driver)
                except Exception:
                    continue
        comparer = PriceComparer(pokemon_box)
        comparer.compare()
        old_data = read_json()
        if old_data is None:
            old_data = []
        old_data.append(pokemon_box.to_dict())
        write_json(old_data)
        logging.info("Saved to price.json")
    finally:
        driver.quit()
if __name__ == "__main__":
    main()