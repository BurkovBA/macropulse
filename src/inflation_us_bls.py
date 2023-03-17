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


# Events schedule is here: https://www.bls.gov/schedule/news_release/cpi.htm


async def generate_telegram_message(tg_api_token):
    # Initialize the bot with your API token
    bot = telegram.Bot(token=tg_api_token)

    await bot.send_photo(chat_id='@MacroPulse', message="Test", parse_mode='html')


if __name__ == '__main__':
    tg_api_token = sys.argv[1]

    try:
        asyncio.run(generate_telegram_message(tg_api_token))
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
