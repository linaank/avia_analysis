from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

import pandas as pd

import airportsdata

# загружаем коды аэропортов
airports = airportsdata.load('IATA')

# отбираем только русские аэропорты
ru_airports = {code: info['city'].lower() for code, info in airports.items() if info['country'] == 'RU'}

# некоторые аэропорты в url ищутся не так как в названии, поэтому меняем
ru_airports["LED"] = 'saint-petersburg'
ru_airports["GOJ"] = 'nizhny-novgorod'
ru_airports["ASF"] = 'astrahan'

codes = ["SVO", "LED", "AER", "GOJ",
         "SVX", "KZN", "OVB", "UFA",
         "KRR", "ROV", "KHV", "VVO", "ASF"]

# формируем список все возможных комбинаций маршрутов
routes = [(o, d) for o in codes for d in codes if o != d]

# список авиакомпаний
companies = ["Россия", "Аэрофлот", "Победа", "S7 Airlines", "Уральские авиалинии"]


options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--user-data-dir=/tmp/selenium_profile")

service = Service()
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)


results = []

for origin, dest in routes:
    url = f"https://travel.yandex.ru/avia/routes/{ru_airports[origin]}--{ru_airports[dest]}"
    driver.get(url)

    # Ждём появления блока с ценами авиакомпаний
    xpath_block = "/html/body/div[1]/div/div[5]/div/div[2]/section/div[1]/div[2]/div[3]"
    try:
        block = wait.until(EC.presence_of_element_located((By.XPATH, xpath_block)))
    except Exception as e:
        print(f"Не удалось загрузить страницу или найти контейнер для маршрута {ru_airports[origin]}–{ru_airports[dest]}: {e}")
        continue

    # Инициализируем словарь с None по умолчанию
    data = {"origin": origin, "dest": dest}
    for comp in companies:
        data[comp] = None

    lines = block.text.splitlines()

    # Идём по парам строк: [название, цена]
    for i in range(0, len(lines), 2):

        name = lines[i].strip()

        # Если встречаем стоп-строку - выходим
        if "Стоимость рейсов с пересадками" in name:
            break

        # Берём цену из следующей строки (если она есть)
        if i + 1 >= len(lines):
            break

        price_text = lines[i + 1]

        # Очищаем текст цены
        price_digits = re.sub(r"\D", "", price_text)
        price = int(price_digits) if price_digits.isdigit() else None

        # Если это одна из нужных компаний - сохраняем
        if name in companies:
            data[name] = price

    results.append(data)

driver.quit()

df = pd.DataFrame(results)
df.to_csv("data/flight_prices.csv", index=False)
print(df.head())
