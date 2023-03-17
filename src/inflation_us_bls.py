import sys
import requests
from io import BytesIO
import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram
from PIL import Image
from bs4 import BeautifulSoup


# Events schedule is here: https://www.bls.gov/schedule/news_release/cpi.htm
url = "https://www.bls.gov/cpi/#"


def get_highcharts_plot():
    options = webdriver.ChromeOptions()

    options.headless = True

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for the element to appear on the page
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-container")))

    # Take a screenshot of element and convert it into a PIL Image object
    pil_image = Image.open(BytesIO(element.screenshot_as_png))

    return pil_image


def get_text():
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the div element with class "nr-entry"
    div_element = soup.find("div", {"class": "nr-entry"})

    # Find the header
    header_element = div_element.find("span", {"class": "heading"})
    header_content = header_element.text.strip()

    # Find the second p element within the div element and get its text content
    second_p_element = div_element.find_all("p")[1]
    first_string = next(iter(second_p_element.contents), None)
    p_content = first_string.split("<br>")[0].strip()
    # p_content = second_p_element.text.strip()

    return header_content, p_content


async def generate_telegram_message(tg_api_token):
    # Initialize the bot with your API token
    bot = telegram.Bot(token=tg_api_token)

    image = get_highcharts_plot()

    # convert PIL image into an in-memory buffer with png
    img_buffer = BytesIO()
    image.save(img_buffer, format='PNG')
    img_buffer.seek(0)  # important to set seek(0), otherwise reading it will return empty result

    header, message = get_text()

    # Create the caption for the post
    caption = f'''
    <u>Вышли <a href="{url}">данные</a> по инфляции в США.</u>

    {header}

    {message}
    '''

    # Upload the image to Telegram and get its file ID
    await bot.send_photo(chat_id='@MacroPulse', photo=img_buffer, caption=caption, parse_mode='html')


if __name__ == '__main__':
    tg_api_token = sys.argv[1]

    try:
        asyncio.run(generate_telegram_message(tg_api_token))
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
