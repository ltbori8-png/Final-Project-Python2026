from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import date


def write_json(data):
    with open('price.json', 'w') as file:
        json.dump(data, file, indent=4)
def read_json():
    try:
        with open('price.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

class Product:
    def __init__(self, name):
        self.name = name
        self.price = {}

    def add_price (self, site, price):
        self.prices[site] = price

    def cheapest_price(self):
        return min(self.price, key=self.price.get)

    def to_dict(self):
        return {
            "date": str(date.today()),
            "name": self.name,
            "prices": self.price,
            "cheapest": self.cheapest_site()
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
        cheapest = self.product.cheapest_site()
        print(f"/nCheapest Site: {cheapest}")
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Edge(options=options)
driver.get("https://www.walmart.com/ip/Pokemon-Scarlet-and-Violet-8-5-Prismatic-Evolutions-Elite-Trainer-Box/13816151308?wmlspartner=wlpa&selectedSellerId=101515736&sourceid=dsn_mpmax_b7816648-c1aa-4cbe-a348-bade7e6d185e&veh=dsn&wmlspartner=dsn_mpmax_b7816648-c1aa-4cbe-a348-bade7e6d185e&cn=00pd_fy27_mp_mp_lo_int_dis_mpmax-p13n&wl9=&wl11=Online&msclkid=0974eb77d1ed1d34b0238175d8df4135")
driver.get("https://www.target.com/p/pokemon-tcg-scarlet-violet-elite-trainer-box-prismatic-evolutions-of-the-pokemon-tcg-1-fully-illustrated-promo-card-9-booster-packs-premium/-/A-1008746912#lnk=sametab")
