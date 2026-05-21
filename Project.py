import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import json
from datetime import datetime
from dataclasses import dataclass, field
import re
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def write_json(data):
    with open("prices.json", 'w') as file:
        json.dump(data, file, indent=4)

def read_json() -> list:
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
        site = self.cheapest_site()
        if site is None:
            return None
        return self.prices[site]

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
        time.sleep(random.uniform(2, 5))
        wait = WebDriverWait(driver, 15)
        item_price = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.css_selector))
        )
        print(item_price.get_attribute("outerHTML"))
        price_text = item_price.get_attribute("textContent").strip()
        print(price_text)
        match = re.search(r"\$?([\d,]+\.\d{2})", price_text)
        if match:
            return float(match.group(1).replace(",", ""))
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
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)
def create_driver():
    driver = webdriver.Edge(options=options)
    driver.set_page_load_timeout(30)
    return driver
pokemon_box = Product ("Pokémon TCG: Scarlet & Violet Elite Trainer Box")
websites = [
    WebsiteScraper(
        "Amazon",
        "https://www.amazon.com/Pokemon-TCG-Scarlet-Violet-Trainer/dp/B0BSNXK3H7/ref=asc_df_B0BSNXK3H7?tag=bingshoppinga-20&linkCode=df0&hvadid=80058400530621&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=95351&hvtargid=pla-4583657880136532&msclkid=9a8a1d99241d169a30f4779e6e772dc9&th=1",
        'span.a-price span.a-offscreen'
    ),
    WebsiteScraper(
        "Walmart",
        "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-and-Violet-Elite-Trainer-Box-Koraidon-Red-1-Full-Art-Promo-Card-9-Boosters-and-Premium-Accessories/2782014366?wmlspartner=wlpa&selectedSellerId=101070956&sourceid=dsn_msft_fead0442-95ce-4933-b538-b3c77293bf8b&veh=dsn&wmlspartner=dsn_msft_fead0442-95ce-4933-b538-b3c77293bf8b&cn=00k9_fy27_mp_mp_lo_int_dis_mpmax&wl9=&wl11=Online&msclkid=e95a424cea9314207da6284ba1d08e8b",
        'span[itemprop="price"]'
    )
]
def main():
    try:
        for site in websites:
            success = False
            for attempt in range(3):
                driver = None
                try:
                    driver = create_driver()
                    price = site.get_price(driver)
                    pokemon_box.add_price(site.site_name, price)
                    print(f"{site.site_name}: ${price}")
                    success = True
                    break
                except Exception as e:
                    logging.error(
                        f"{site.site_name} attempt {attempt + 1} failed: {e}"
                    )
                finally:
                    if driver:
                        driver.quit()
            if not success:
                logging.error(f"{site.site_name} failed after 3 attempts")
        comparer = PriceComparer(pokemon_box)
        comparer.compare()
        old_data = read_json()
        old_data.append(pokemon_box.to_dict())
        write_json(old_data)
        logging.info("Saved to price.json")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
if __name__ == "__main__":
    main()