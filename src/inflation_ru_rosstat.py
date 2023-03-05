import re
import datetime
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_url():
    current_date = datetime.today().strftime('%d-%m-%y')
    pattern = f'https://rosstat.gov.ru/storage/mediabank/(\d+_{current_date}).html'
    
    news_page = 'https://rosstat.gov.ru/central-news'
    response = requests.get(news_page)
    match = re.search(pattern, response.text)
    
    return match.group(1)

def get_image():
    # Set up the Chrome driver
    driver = webdriver.Chrome()

    # get page url
    url = get_url()
    
    # Load the webpage
    driver.get(url)

    # Wait for the element to appear on the page
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "element-id")))

    # Take a screenshot of the element
    element_screenshot = element.screenshot_as_png

    # Quit the driver
    driver.quit()

if __name__ == '__main__':
    get_image()
