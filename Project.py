from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import date

def write_json(data):
    with open("prices.json", 'w') as file:
        json.dump(data, file, indent=4)

def read_json():
    try:
        with open("prices.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

class Product:
    def __init__(self, name):
        self.name = name
        self.prices = {}

    def add_price(self, site, price):
        self.prices[site] = price

    def cheapest_site(self):
        return min(self.prices, key=self.prices.get)

    def cheapest_price(self):
        return self.prices[self.cheapest_site()]

    def to_dict(self):
        return {
            "Date": str(date.today()),
            "Name": self.name,
            "Prices": self.prices,
            "Cheapest Site": self.cheapest_site(),
            "Cheapest Price": self.cheapest_price()
        }

class WebsiteScrapper:
    def __init__(self, site_name, url, css_selector):
        self.site_name = site_name
        self.url = url
        self.css_selector = css_selector

    def get_price(self, driver):
        driver.get(self.url)
        wait = WebDriverWait(driver, 10)
        item_price = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.css_selector)
            )
        )
        price_text = item_price.text
        cleaned_price = (
            price_text.replace("$", "").replace(",", "").strip()
        )
        return float(cleaned_price)

class PriceComparer:
    def __int__(self, product):
        self.product = product

    def compare(self):
        cheapest_site = self.product.cheapest_site()
        cheapest_price = self.product.cheapest_price()
        for site, price in self.product.prices.items():
            print(f"{site}: ${price}")
        print("\nCheapest Site: ", cheapest_site)
        print("\nCheapest Price: $", cheapest_price)


def main():
    options = webdriver.EdgeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Edge(options=options)
    pokemon_box = Product ("Pokemon TCG: Scarlet & Violet: Prismatic Elite Box")
    websites = [
        WebsiteScrapper(
            "Walmart",
            "https://www.walmart.com/ip/Pokemon-Scarlet-and-Violet-8-5-Prismatic-Evolutions-Elite-Trainer-Box/13816151308?wmlspartner=wlpa&selectedSellerId=101515736&sourceid=dsn_mpmax_b7816648-c1aa-4cbe-a348-bade7e6d185e&veh=dsn&wmlspartner=dsn_mpmax_b7816648-c1aa-4cbe-a348-bade7e6d185e&cn=00pd_fy27_mp_mp_lo_int_dis_mpmax-p13n&wl9=&wl11=Online&msclkid=0974eb77d1ed1d34b0238175d8df4135",
            '[itemprop="price"]'
        ),
        WebsiteScrapper(
            "Target",
            "https://www.target.com/p/pokemon-tcg-scarlet-violet-elite-trainer-box-prismatic-evolutions-of-the-pokemon-tcg-1-fully-illustrated-promo-card-9-booster-packs-premium/-/A-1008746912#lnk=sametab",
            '[data-test="product-price"]'
        )
    ]
    for site in websites:
        try:
            price = site.get_price(driver)
            pokemon_box.add_price(site.site_name,price)
            print(f"{site.site_name}: ${price}")
        except Exception as e:
            print(f"There's been an error in scraping from {site.site_name}: {e}... sorry")
            comparer = PriceComparer()
            comparer.compare()
            old_data = read_json()
            old_data.append(
                pokemon_box.to_dict()
            )
            write_json(old_data)
            print("\nSaved to price.json")
            driver.quit()

    if __name__ == "__main__":
        main()