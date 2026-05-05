import Class
import selenium
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

class PriceEntry:
    def __init__(self, entry_date, price):
        self.date = entry_date
        self.price = price

    def to_dict(self):
        return {
            "date": self.date,
            "price": self.price,
        }