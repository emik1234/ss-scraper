import os
import sys
from contextlib import redirect_stderr

# Suppress TensorFlow warnings completely
sys.stderr = open(os.devnull, 'w')  # Nuclear option - use cautiously!
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress ALL messages

# Restore stderr later if needed (after your imports)
# sys.stderr = sys.__stderr__

from scraper import retrieve_data, set_filters
from prompts import get_input
from selenium import webdriver
from excel import export_to_excel

if __name__ == "__main__":
    data = get_input()

    # get a base value for creating the heap
    excel_filter = input("Izvēlieties Excel filtrus: gads, tilpums, nobraukums, cena ->")
    excel_filter = excel_filter.strip()

    driver = webdriver.Chrome()

    try:
        filters = set_filters(driver, data)

        if filters:
            result = retrieve_data(driver, excel_filter)
            export_to_excel(result)
    finally:
        driver.quit()