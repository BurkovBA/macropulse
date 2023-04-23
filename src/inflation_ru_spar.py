import sys
import requests
import asyncio
from io import BytesIO

import telegram
from bs4 import BeautifulSoup
import matplotlib
import seaborn as sns
import pandas as pd
import dataframe_image as dfi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# keys in the basket are the goods, values are dicts with urls in online shop and weights
basket = {
    "Лук репчатый":                   {"url": "https://myspar.ru/catalog/ovoshchi/luk-repchatyy/",                                                  "weight": 1},
    "Капуста белокачанная":           {"url": "https://myspar.ru/catalog/ovoshchi/kapusta-belokochannaya/",                                         "weight": 1},
    "Яблоки сезонные":                {"url": "https://myspar.ru/catalog/frukty/yabloki-sezonnye/",                                                 "weight": 1},
    "Свекла красная":                 {"url": "https://myspar.ru/catalog/ovoshchi/svekla/",                                                         "weight": 1},
    "Курица филе":                    {"url": "https://myspar.ru/catalog/ptitsa/file-kurinoe-ves/",                                                 "weight": 1},
    "Молоко Простоквашино, 3.2%":     {"url": "https://myspar.ru/catalog/moloko/moloko-prostokvashino-otbornoe-3-4-4-5-plastikovaya-butylka-930g/", "weight": 1},
    "Масло сливочное":                {"url": "https://myspar.ru/catalog/maslo-margarin/maslo-spar-slivochnoe-traditsionnoe-82-5-100g/",            "weight": 1},
    "Перец микс":                     {"url": "https://myspar.ru/catalog/ovoshchi/perets-miks-400g/",                                               "weight": 1},
    "Огурцы короткоплодные":          {"url": "https://myspar.ru/catalog/ovoshchi/ogurtsy-korotkoplodnye/",                                         "weight": 1},
    "Груша":                          {"url": "https://myspar.ru/catalog/frukty/grushi-pakkham/",                                                   "weight": 1},
    "Картофель":                      {"url": "https://myspar.ru/catalog/ovoshchi/kartofel/",                                                       "weight": 1},
    "Киви":                           {"url": "https://myspar.ru/catalog/frukty/kivi/",                                                             "weight": 1},
    "Огурцы тепличные среднеплодные": {"url": "https://myspar.ru/catalog/ovoshchi/ogurtsy-teplichnye-sredneplodnye/",                               "weight": 1},
    "Морковь":                        {"url": "https://myspar.ru/catalog/ovoshchi/morkov/",                                                         "weight": 1},
    "Капуста цветная":                {"url": "https://myspar.ru/catalog/ovoshchi/kapusta-tsvetnaya/",                                              "weight": 1},
    "Баклажаны с овощами":            {"url": "https://myspar.ru/catalog/ovoshchnaya-konservatsiya-1/baklazhany-spar-s-ovoshchami-520g/",           "weight": 1},
    "Кабачки":                        {"url": "https://myspar.ru/catalog/ovoshchi/kabachki/",                                                       "weight": 1},
    "Песок сахарный 1 кг":            {"url": "https://myspar.ru/catalog/sakhar/pesok-sakharnyy-1-kg/",                                             "weight": 1},
    "Крупа гречневая 900г":           {"url": "https://myspar.ru/catalog/krupy/grecha-spar-900g/",                                                  "weight": 1}
}

spar_search_base_url = 'https://myspar.ru/#search?query='


def get_current_prices():
    prices = {}  # {product_name: price}

    for product_name in basket:
        options = webdriver.ChromeOptions()

        options.headless = True

        # Set up the Chrome driver
        driver = webdriver.Chrome(options=options)

        # Load the webpage
        driver.get(basket[product_name]['url'])

        # Wait for the element to appear on the page
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "prices__cur")))
        price = float(element.text.split()[0]) / 100

        prices[product_name] = price

    return prices


def get_table_image(df):
    buffer = BytesIO()
    dfi.export(df, buffer)
    buffer.seek(0)

    return buffer


def get_inflation(current_prices, previous_prices):
    inflation = 0
    for product_name in basket:
        inflation += basket[product_name]['weight'] * (current_prices[product_name] - previous_prices[product_name])

    return inflation


async def generate_telegram_message(tg_api_token):
    # Initialize the bot with your API token
    bot = telegram.Bot(token=tg_api_token)

    prices = get_current_prices()
    df = pd.DataFrame.from_dict(prices, orient='index')
    img_buffer = get_table_image(df)

    inflation = get_inflation(prices, prices)

    # Create the caption for the post
    caption = f'''
<u>Инфляция за неделю в России, рассчитанная по ценам в Spar</u>

Новое значение инфляции: <b>{inflation}%</b>.
    '''

    # Upload the image to Telegram and get its file ID
    await bot.send_photo(chat_id='@MacroPulse', photo=img_buffer.getvalue(), caption=caption, parse_mode='html')


if __name__ == '__main__':
    tg_api_token = sys.argv[1]

    try:
        asyncio.run(generate_telegram_message(tg_api_token))
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
