import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import date
import requests

def write_json(data):
    with open('price.json', 'w') as file:
        json.dump(data, file, indent=4)
def read_json():
    try:
        with open('price.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

class PriceEntry:
    def __init__(self, entry_date, price):
        self.date = entry_date
        self.price = price

    def to_dict(self):
        return {
            "date": self.date,
            "price": self.price
        }

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
options.add_argument("headless")
driver = webdriver.Edge(options=options)
driver.get("https://www.amazon.com/Pokemon-TCG-Scarlet-Violet-Prismatic-Evolutions/dp/B0DLPL7LC5/ref=asc_df_B0DLPL7LC5?tag=bingshoppinga-20&linkCode=df0&hvadid=80883033960730&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=95351&hvtargid=pla-4584482509038924&psc=1&msclkid=b87c67c97e491f0c1b610e336bac0581")
print(driver.title)

wait = WebDriverWait(driver, 10)
item_price = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='product-price']"))
)
print(item_price.text)
price_value = float(item_price.text.replace("$", "").replace(",", "").strip())
today = str(date.today())
new_entry = PriceEntry(today, price_value)

data = read_json()
if data is None:
    data = []
data.append(new_entry.to_dict())