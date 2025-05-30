import re

def normalize_brand(brand: str) -> str:
    """Normalize manufacturer name and car name to ss.lv supported version (lowercase, `-` seperator)"""

    brand = brand.strip().lower()
    brand = re.sub(r'[\s_]+', '-', brand)
    brand = re.sub(r'[^a-z0-9-]', '', brand)
    return brand


def validate_year(year_text: str):
    """Validate whether user's entered year is a number between 1900 and 2025"""

    return year_text.isdigit() and 1900 <= int(year_text) <= 2025


def ask_input(prompt: str, validator=None, choices=None, normalizer=None, required=False, default=None) -> str:
    """Prompt user for input and validate the answer"""

    while True:
        value = input(f"{prompt}")
        value = value.strip()

        if not value and default is not None:
            value = default

        if value and choices:
            if normalizer(value) not in choices:
                print("Nederīga atbilde.")
                continue

        if required and not value:
            print("Šis lauks ir obligāts.")
            continue

        if validator and value and not validator(value):
            print("Nederīga atbilde.")
            continue
        
        if normalizer and value:
            value = normalizer(value)

        return value


def get_input() -> dict:
    """Prompts user for input data. Returns a dictionary containing the data."""

    print("--------- AUTOMAŠĪNU MEKLĒTĀJS ---------\n")
    print("Nosacījumi: mašīnas markai un modelim raksti pilno nosaukumu. Neobligātajiem laukiem var atstāt tukšas atbildes.\n")

    max_price = ask_input(
        "Maksimālā cena:",
        required=False
    )

    brand = ask_input(
        "Automašīnas marka*:",
        normalizer=normalize_brand,
        required=True
    )
    model = ask_input(
        "Automašīnas modelis*:",
        normalizer=normalize_brand,
        required=True
    )
    min_year = ask_input(
        "Mašīnas vecums (sākot no):",
        validator=validate_year,
        required=False
    )
    engine = ask_input(
        "Mašīnas degvielas veids (Benzīns / Dīzelis / Benzīns/gāze / Hibrīds):",
        normalizer=str.capitalize,
        choices=["Benzīns", "Dīzelis", "Benzīns/gāze", "Hibrīds"],
        required=False
    )
    transmission = ask_input(
        "Pārnesumkārba (Automāts / Manuāla):",
        normalizer=str.capitalize,
        choices=["Automāts", "Manuāla"],
        required=False
    )
    engine_size = ask_input(
        "Tilpums (sākot no):",
        required=False
    )
    color = ask_input(
        "Krāsa:",
        required=False
    )
    build = ask_input(
        "Virsbūves tips:",
        required=False
    )

    return {
        'brand': brand,
        'model': model,
        'max_price': max_price,
        'min_year': min_year,
        'engine': engine,
        'transmission': transmission,
        'engine_size': engine_size,
        'color': color,
        'build': build
    }


if __name__ == "__main__":
    get_input()