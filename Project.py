import selenium
import By
import WebDriverWait
import expected_conditions as EC
import json
import date

def write_json(data):
    with open('price.json', 'w'):