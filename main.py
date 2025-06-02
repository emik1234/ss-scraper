from scraper import retrieve_data, set_filters
from prompts import get_input
from selenium import webdriver

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
    finally:
        driver.quit()