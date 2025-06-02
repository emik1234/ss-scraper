from prompts import get_input
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from heapfile import MaxHeap, MinHeap, Car
import re

URL = "https://www.ss.com/lv/transport/cars/"

def set_filters(driver, data: dict) -> bool:
    """Sets user-specified filter in the website"""

    try:
        # construct model url
        url = f"{URL}{data['brand']}/{data['model']}/filter"

        driver.get(url)

        # select max price from the select box
        if data['max_price']:
            max_price_box = driver.find_element(By.NAME, "topt[8][max]")
            max_price_box.send_keys(data['max_price'])

        # select min year from the select box
        if data['min_year']:
            find_data(driver, "topt[18][min]", data['min_year'], "minimālais gads", True)

        # select engine type from the select box
        if data['engine']:
            find_data(driver, "opt[34]", data['engine'], "dzinēja veids")

        # select transmission from the select box
        if data['transmission']:
            find_data(driver, "opt[35]", data['transmission'], "transmisijas veids")
            
        # select min engine size from the select box
        if data['engine_size']:
            find_data(driver, "topt[15][min]", data['engine_size'], "dzinēja tilpums", True)

        # select color from the select box
        if data['color']:
            find_data(driver, "opt[17]", data['color'], "krāsas veids")

        # apply filters
        driver.find_element(By.XPATH, '//input[@value="Meklēt"]').click()

        return True
    except:
        print("Nepareizi ievadīta mašīnas marka! Pārbaudiet ievadītos datus.")
        return False



def find_data(driver, box_name: str, data_to_select: str, error_message: str, set_next_best=False):
    """Find specified filters' input box and apply the filter to the specified value"""

    try:
        # find select box and select corresponding data
        box = driver.find_element(By.NAME, box_name)
        select = Select(box)
        select.select_by_visible_text(data_to_select)
    except:
        set_next_best_value(driver, box_name, data_to_select, error_message) if set_next_best else print(f"Nav atrasts norādītais {error_message}")


def set_next_best_value(driver, box_name: str, value: str, error_message: str):
    """Sets the next best value for filters like min year or min engine size if specified isn't an available option"""

    try:
        available_value = None

        box = driver.find_element(By.NAME, box_name)
        select = Select(box)

        # iterate through all available options and find the closest one that is larger
        for option in reversed(select.options):
            try:
                dropdown_value = float(option.text)

                if not available_value:
                    available_value = float(dropdown_value)
                    continue
                
                if dropdown_value >= float(value) and dropdown_value < available_value:
                    available_value = float(dropdown_value)
            except ValueError:
                continue
        if available_value != None:
            # check if the value is a float or an int and set the value
            try:
                float(available_value)
                select.select_by_visible_text(str(available_value))
            except:
                select.select_by_visible_text(str(int(available_value)))                
        else:
            print(f"Nav atrasts norādītais {error_message} robežu ietvaros.")
    except Exception as e:
        print(e)


def retrieve_data(driver, excel_filter) -> list:
    """Find table containing data about all cars and scrape them individually. Go to next page if one exists."""
    next_page = True
    
    # get a base value for creating the heap

    # heap creation
    match excel_filter:
        case "gads":
            heap = MaxHeap(parameter=lambda car: car.year)
        case "tilpums":
            heap = MaxHeap(parameter=lambda car: car.engine_size)
        case "nobraukums":
            heap = MinHeap(parameter=lambda car: car.mileage)
        case "cena":
            heap = MinHeap(parameter= lambda car: car.price)    
    

    while next_page:
        driver.execute_script("window.scrollTo(0, 0);")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))   

        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # find filter nested inside the parent table
            table_parent = driver.find_element(By.TAG_NAME, "table").find_element(By.ID, "filter_frm")

            # find all nested tables and select one including data about cars
            table = table_parent.find_elements(By.TAG_NAME, "table")[2]

            # retrieve all rows about cars
            cars = table.find_elements(By.TAG_NAME, "tr")


            # iterate through each car
            for car in cars[1:-1]:
                try:
                    # get all data
                    all_data = car.find_elements(By.TAG_NAME, "td")
                    
                    # extract specific data from all data
                    link = all_data[1].find_element(By.TAG_NAME, "a").get_attribute('href')
                    text = all_data[2].text
                    year = int(all_data[3].text)
                    engine_size = float(all_data[4].text)
                    mileage = all_data[5].text
                    mileage = int(re.search(r'\d+[\.,]?\d*', mileage).group().replace(',', ''))
                    price = all_data[6].text
                    price = int(re.search(r'\d+[\.,]?\d*', price).group().replace(',', ''))

                    print(link, text, year, engine_size, mileage, price)

                    # add to heap, in which comparison operations are made in regards to the user inputted attribute
                    heap.insert(Car(link, text, year, engine_size, mileage, price))
                    
                    print("Added successfully)")
                except:
                    print("error")
                    continue
            
            try:
                # try to find all pagination buttons with rel="next"
                next_page_btns = driver.find_elements(By.CSS_SELECTOR, 'a[name="nav_id"][rel="next"]')

                next_page = False
                
                # check if next page exists
                for button in next_page_btns:
                    if button.text != "Nākamie":
                        next_page = True

                # go to next page if exists
                if next_page:
                    driver.find_element(By.XPATH, '//a[text()="Nākamie "]').click()
            except Exception as e:
                print(f"Kļūda datu apstrādē: {e}")
                next_page = False
        except Exception as e:
            print(f"Kļūda datu apstrādē: {e}")

    if len(heap.heap) == 0:
        print("Netika atrasta neviena mašīna ar šiem filtriem!")

    print("Meklēšana pabeigta!")

    return heap


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

    print("test")
    print(result)
    test = result.remove()
    print("worked")
    print(test.price)
    test = result.remove()
    print(test.mileage)
    

