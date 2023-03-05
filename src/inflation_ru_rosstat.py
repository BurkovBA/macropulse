import sys
import requests
import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram
from bs4 import BeautifulSoup
import pandas as pd


def get_page_url():
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


def get_main_text(url):
    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    p_P7 = soup.find('p', {'class': 'P7'})
    span_T11 = p_P7.find_all('span', {'class': 'T11'})

    return "".join([span.text for span in span_T11])


def get_image(url):
    # Set up the Chrome driver
    driver = webdriver.Chrome()
    
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


def get_table(url):
    # Name of the class of the table HTML element
    table_class = 'Table2'

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table element by class name
    table = soup.find('table', {'class': table_class})

    # Extract the table data into a list of lists
    data = []
    rows = table.find_all('tr')
    for row in rows[3:]:  # first 3 rows are header
        cells = row.find_all('td')
        data.append([cell.text.strip() for cell in cells])

    # Create a Pandas DataFrame from the table data
    df = pd.DataFrame(
        data[1:],
        columns=["Продукт", "Изменение цены на этой неделе", "Прошлая неделя", "Прошлый месяц", "Прошлый год"],
    )
    df["Изменение цены на этой неделе"] = df["Изменение цены на этой неделе"].str.replace(',', '.').astype(float)
    df["Прошлая неделя"] = df["Прошлая неделя"].str.replace(',', '.').astype(float)
    df["Прошлый месяц"] = df["Прошлый месяц"].str.replace(',', '.').astype(float)
    df["Прошлый год"] = df["Прошлый год"].str.replace(',', '.').astype(float)

    return df


def detect_outliers(df):
    row = df.iloc[:, 1]

    # Calculate the IQR of the row
    q1 = row.quantile(0.25)
    q3 = row.quantile(0.75)
    iqr = q3 - q1

    # Calculate the upper and lower bounds for outliers
    lower_bound = q1 - (3 * iqr)
    upper_bound = q3 + (3 * iqr)

    # Find the values in the row that are outside the bounds
    outliers = row[(row < lower_bound) | (row > upper_bound)]

    return outliers


async def generate_telegram_message(tg_api_token):
    url = get_page_url()

    # Initialize the bot with your API token
    bot = telegram.Bot(token=tg_api_token)

    # get image
    image = get_image(url)

    # get main text
    main_text = get_main_text(url)

    # get table with specific goods
    table = get_table(url)

    # prepare the text on outliers
    outliers = detect_outliers(table)
    outliers_text = "\n".join([f"{table.iloc[outlier_index]['Продукт']}: {outlier_value}%" for outlier_index, outlier_value in outliers.iteritems()])

    # Create the caption for the post
    caption = f'''
<u>Вышла <a href="{url}">статистика</a> по инфляции в России за последнюю неделю.</u>

{main_text}

Существенно изменилась стоимость следующих товаров:

{outliers_text}
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
