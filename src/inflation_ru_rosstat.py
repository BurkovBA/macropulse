import sys
import requests
import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram
from bs4 import BeautifulSoup


def get_url():
    # get the catalog page with news
    news_page = 'https://rosstat.gov.ru/central-news'
    response = requests.get(news_page)

    # Create a BeautifulSoup object from the HTML string
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first anchor element that contains the specified text
    link_element = soup.find('a', text=lambda t: t and 'Об оценке индекса потребительских цен' in t)

    # Get the URL of the link element
    link_url = link_element['href']

    return "https://rosstat.gov.ru" + link_url


def get_image():
    # Set up the Chrome driver
    driver = webdriver.Chrome()

    # get page url
    url = get_url()
    
    # Load the webpage
    driver.get(url)

    # Wait for the element to appear on the page
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Table1")))

    # Take a screenshot of the element
    element_screenshot = element.screenshot_as_png

    # Quit the driver
    driver.quit()

    return element_screenshot


async def generate_telegram_message(tg_api_token):
    url = get_url()

    # Initialize the bot with your API token
    bot = telegram.Bot(token=tg_api_token)

    # get image from RosStat
    image = get_image()

    # Create the caption for the post
    caption = f'''
<u>Вышла <a href="{url}">статистика</a> по инфляции в России за последнюю неделю.</u>

TODO: Больше текстовых подробностей и анализа.
    '''

    # Upload the image to Telegram and get its file ID
    await bot.send_photo(chat_id='@MacroPulse', photo=image, caption=caption, parse_mode='html')
    # photo_id = photo.photo[-1].file_id

    # Send the post to Telegram
    # await bot.send_photo(chat_id='@MacroPulse', photo=photo_id, caption=caption)


if __name__ == '__main__':
    tg_api_token = sys.argv[1]

    try:
        asyncio.run(generate_telegram_message(tg_api_token))
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
