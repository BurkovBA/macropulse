import re
import datetime
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram
from bs4 import BeautifulSoup


def get_url(current_date=None):
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


def generate_telegram_message():
    # Initialize the bot with your API token
    bot = telegram.Bot(token='YOUR_API_TOKEN')

    # Upload the image to Telegram and get its file ID
    photo = bot.send_photo(chat_id='@CHANNEL_OR_CHAT_ID', photo=open('image.jpg', 'rb'))
    photo_id = photo.photo[-1].file_id

    # Create the caption for the post
    caption = 'This is a caption for the image'

    # Send the post to Telegram
    bot.send_photo(chat_id='@CHANNEL_OR_CHAT_ID', photo=photo_id, caption=caption)


if __name__ == '__main__':
    get_image()
