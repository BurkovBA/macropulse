import sys
import requests
import asyncio
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram
from bs4 import BeautifulSoup
import pandas as pd
from PIL import Image


# Calender: https://www.cbr.ru/dkp/cal_mp/
url = "https://www.cbr.ru/eng/hd_base/KeyRate/"


def get_plot():
    # Set screen resolution
    options = webdriver.ChromeOptions()

    options.headless = True

    options.add_argument('--window-size=2560,1440')  # set screen resolution to 2560x1440 or 1920x1080

    # Set zoom level
    options.add_argument('--force-device-scale-factor=.25')  # set zoom level to 25%

    # Set up the Chrome driver
    driver = webdriver.Chrome(options=options)

    # Load the webpage
    driver.get(url)

    # Wait for the element to appear on the page
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-container")))

    # Take a screenshot of element and convert it into a PIL Image object
    pil_image = Image.open(BytesIO(element.screenshot_as_png))

    # Quit the driver
    driver.quit()

    return pil_image


def get_key_interest_rate():
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the div element with class "nr-entry"
    data_table_element = soup.find("table", {"class": "data"})

    # Find the second tr element within the div element and get its text content
    second_tr_element = data_table_element.find_all("tr")[1]
    second_td_element = second_tr_element.find_all("td")[1]

    interest_rate = second_td_element.text

    return interest_rate


async def generate_telegram_message(tg_api_token):
    # Initialize the bot with your API token
    bot = telegram.Bot(token=tg_api_token)

    image = get_plot()

    # convert PIL image into an in-memory buffer with png
    img_buffer = BytesIO()
    image.save(img_buffer, format='PNG')
    img_buffer.seek(0)  # important to set seek(0), otherwise reading it will return empty result

    key_interest_rate = get_key_interest_rate()

    # Create the caption for the post
    caption = f'''
    <u>Состоялось заседание по <a href="{url}">ключевой ставке Центрального банка РФ</a></u>

    Новое значение ключевой ставки: <b>{key_interest_rate}</b>.
    '''

    # Upload the image to Telegram and get its file ID
    await bot.send_photo(chat_id='@MacroPulse', photo=img_buffer, caption=caption, parse_mode='html')


if __name__ == '__main__':
    tg_api_token = sys.argv[1]

    try:
        asyncio.run(generate_telegram_message(tg_api_token))
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
