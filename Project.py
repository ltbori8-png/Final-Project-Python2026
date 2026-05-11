import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import date
import requests
from bs4 import BeautifulSoup

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
    def __init__(self, name, site, url, tag, class_name):
        self.name = name
        self.site = site
        self.url = url
        self.tag = tag
        self.class_name = class_name
        self.price = None

    def to_dict(self):
        return {
            "name": self.name,
            "site": self.site,
            "url": self.url,
            "price": self.price
        }

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Edge(options=options)
driver.get("https://www.walmart.com/ip/Pokemon-Scarlet-and-Violet-8-5-Prismatic-Evolutions-Elite-Trainer-Box/13816151308?wmlspartner=wlpa&selectedSellerId=101515736&sourceid=dsn_mpmax_b7816648-c1aa-4cbe-a348-bade7e6d185e&veh=dsn&wmlspartner=dsn_mpmax_b7816648-c1aa-4cbe-a348-bade7e6d185e&cn=00pd_fy27_mp_mp_lo_int_dis_mpmax-p13n&wl9=&wl11=Online&msclkid=0974eb77d1ed1d34b0238175d8df4135")
driver.get("https://www.target.com/p/pokemon-tcg-scarlet-violet-elite-trainer-box-prismatic-evolutions-of-the-pokemon-tcg-1-fully-illustrated-promo-card-9-booster-packs-premium/-/A-1008746912#lnk=sametab")
print(driver.title)

wait = WebDriverWait(driver, 10)
item_price = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='product-price']"))
)
print(item_price.text)
price_value = float(item_price.text.replace("$", "").replace(",", "").strip())
today = str(date.today())
new_entry = Product(today, price_value)

data = read_json()
if data is None:
    data = []
data.append(new_entry.to_dict())