import pandas as pd
from scraper import retrieve_data, set_filters
from prompts import get_input
from selenium import webdriver
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

def export_to_excel(car_heap, file_name="auto_dati.xlsx"):
    """Saglabā automašīnu sarakstu Excel failā"""
    if not car_heap or not car_heap.heap:
        print("Nav datu, ko saglabāt.")
        return

    # Pārveido datus no heap uz list of dicts
    data = [{
        "Saite": car.link,
        "Īss apraksts": car.text,
        "Gads": car.year,
        "Tilpums (L)": car.engine_size,
        "Nobraukums (tūkst. km)": car.mileage,
        "Cena (€)": car.price
    } for car in car_heap.heap]

    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    print(f"Dati saglabāti failā: {file_name}")


################## FORMATĒJUMS ######################

    wb = load_workbook(file_name)
    ws = wb.active

    # Iesaldē virsraksta rindu
    ws.freeze_panes = "A2"

    # Formatēt virsrakstus
    for col_num, column_cells in enumerate(ws.iter_cols(min_row=1, max_row=1), start=1):
        max_length = max(len(str(cell.value)) for cell in column_cells)
        col_letter = get_column_letter(col_num)

        # Pielāgo kolonnas platumu
        ws.column_dimensions[col_letter].width = max(max_length + 2, 15)

        # Stilē virsrakstu (treknraksts + centrēts)
        for cell in column_cells:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')

    # Formatē cenas kā valūtu
    for row in ws.iter_rows(min_row=2, min_col=6, max_col=6):
        for cell in row:
            cell.number_format = '#,## €'

    wb.save(file_name)

############### ^^^^^^^^^^^^ FORMATĒJUMS ^^^^^^^^^^^^^^^ ################################


if __name__ == "__main__":
    # Lietotāja ievade
    data = get_input()

    # Kurš filtrs jāizmanto kā kārtošanas kritērijs
    excel_filter = input("Izvēlieties Excel filtrus: gads, tilpums, nobraukums, cena ->").strip()

    # Palaist pārlūku
    driver = webdriver.Chrome()

    try:
        filters = set_filters(driver, data)
        if filters:
            car_heap = retrieve_data(driver, excel_filter)
            export_to_excel(car_heap)
    finally:
        driver.quit()
