import datetime
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


def get_url():
    now = datetime.datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    url = f"https://www.federalreserve.gov/newsevents/pressreleases/monetary{year}{month}{day}a.htm"

    return url


def get_release_text(url):
    if not url:
        url = get_url()
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the div element with class "releaseInfo"
    div_element = soup.find("div", {"id": "article"})

    # Find the second tr element within the div element and get its text content
    third_child_div = div_element.find_all("div")[2]

    release_text = third_child_div.text

    return release_text


async def generate_telegram_message(tg_api_token):
    # Initialize the bot with your API token
    bot = telegram.Bot(token=tg_api_token)

    url = "https://www.federalreserve.gov/newsevents/pressreleases/monetary20230201a.htm"
    text = get_release_text(url)

    # Create the caption for the post
    caption = f'''
<u>Состоялось заседание по <a href="{url}">ключевой ставке ФРС США</a></u>

Текст пресс-релиза:
{text}
    '''

    # Upload the image to Telegram and get its file ID
    await bot.send_message(chat_id='@MacroPulse', message=text, parse_mode='html')


if __name__ == '__main__':
    tg_api_token = sys.argv[1]

    try:
        asyncio.run(generate_telegram_message(tg_api_token))
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
