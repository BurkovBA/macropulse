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
url = "https://www.cbr.ru/statistics/ms/"


def get_image():
    options = webdriver.ChromeOptions()

    options.headless = True

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for the element to appear on the page
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "xc-uicomponent")))

    # Take a screenshot of element and convert it into a PIL Image object
    pil_image = Image.open(BytesIO(element.screenshot_as_png))

    return pil_image


def get_money_supply():
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the div element with class "nr-entry"
    div_element = soup.find("div", {"id": "xc-label-div-xgen_2926"})
    div_content = div_element.text.strip()

    return div_content


async def generate_telegram_message(tg_api_token):
    # Initialize the bot with your API token
    bot = telegram.Bot(token=tg_api_token)

    image = get_image()

    # convert PIL image into an in-memory buffer with png
    img_buffer = BytesIO()
    image.save(img_buffer, format='PNG')
    img_buffer.seek(0)  # important to set seek(0), otherwise reading it will return empty result

    key_interest_rate = get_money_supply()

    # Create the caption for the post
    caption = f'''
<u>Вышли данные по <a href="{url}">денежной массе М2 в России</a> на начало прошедшего месяца</u>

Денежная масса составляла <b>{key_interest_rate}</b> миллиардов рублей.
    '''

    # Upload the image to Telegram and get its file ID
    await bot.send_photo(chat_id='@MacroPulse', photo=img_buffer, caption=caption, parse_mode='html')


if __name__ == '__main__':
    tg_api_token = sys.argv[1]

    try:
        asyncio.run(generate_telegram_message(tg_api_token))
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
