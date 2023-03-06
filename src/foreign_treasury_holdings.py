import sys
import requests
import asyncio
from io import StringIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram
from bs4 import BeautifulSoup
import pandas as pd


url = "https://ticdata.treasury.gov/Publish/mfh.txt"


def get_pre_as_image():
    # Set screen resolution
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=2560,1440')  # set screen resolution to 2560x1440 or 1920x1080

    # Set zoom level
    options.add_argument('--force-device-scale-factor=.25')  # set zoom level to 25%

    # Set up the Chrome driver
    driver = webdriver.Chrome(options=options)

    # Load the webpage
    driver.get(url)

    # Wait for the element to appear on the page
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "Pre")))

    # Take a screenshot of the element
    element_screenshot = element.screenshot_as_png

    # Quit the driver
    driver.quit()

    return element_screenshot


def get_pre_as_dataframe():
    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    text = response.content.decode("utf-8")

    prefix = '------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------\r\n\r\n'
    suffix = 'Of which:'

    text_without_prefix = text.split(prefix)[-1]

    suffix_index = text_without_prefix.index(suffix)
    text_without_prefix_and_suffix = text_without_prefix[:suffix_index].strip()
    print(text_without_prefix_and_suffix)
    csvStringIO = StringIO(text_without_prefix_and_suffix)

    df = pd.read_csv(csvStringIO, sep='\s\s+', names=['Country', '1 month ago', '2 months ago', '3 months ago', '4 months ago', '5 months ago', '6 months ago', '7 months ago', '8 months ago', '9 months ago', '10 months ago', '11 months ago', '12 months ago', '13 months ago'])

    return df


def get_plot(df):
    return


async def generate_telegram_message(tg_api_token):
    # Initialize the bot with your API token
    bot = telegram.Bot(token=tg_api_token)

    # get image
    image = get_pre_as_image()

    # get dataframe
    df = get_pre_as_dataframe(url)

    # get line chart of dynamics
    plot = get_plot(df)

    # Create the caption for the post
    caption = f'''
<u>Вышла <a href="{url}">статистика</a> по изменению позиций иностранных держателей в US Treasuries.</u>
    '''

    # Upload the image to Telegram and get its file ID
    await bot.send_photo(chat_id='@MacroPulse', photo=image, caption=caption, parse_mode='html')


if __name__ == '__main__':
    tg_api_token = sys.argv[1]

    try:
        asyncio.run(generate_telegram_message(tg_api_token))
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
