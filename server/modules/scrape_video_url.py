import json
import requests

from selenium import webdriver
from selenium.webdriver.common.bidi.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.common.log import Log
from playwright.sync_api import sync_playwright


async def scrape_video_url():
    url = 'https://www.arte.tv/fr/videos/RC-014085/arte-journal/'
    with sync_playwright() as p:
        # open video index
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        video_link = page.query_selector('a[data-testid="ts-tsItemLink"]').get_attribute("href")
        page.context.close() 
        browser.close()
        
        print(video_link) 
        # Video lnk example: /fr/videos/117014-031-A/arte-journal/
        # API link example: https://api.arte.tv/api/player/v2/config/fr/117014-031-A
        api_link = f'https://api.arte.tv/api/player/v2/config/fr/{video_link.replace("/fr/videos/","").replace("/arte-journal/", "")}'
        response = requests.get(api_link).json()
        return response["data"]["attributes"]["streams"][0]["url"]

    # browser = webdriver.Chrome()
    # browser.get(url)
    # first_video_link = browser.find_element(By.CSS_SELECTOR, '[data-testid="ts-tsItemLink"]')  # Find the search box

    # video_page = first_video_link.get_attribute("href")
    # print(video_page)
    # browser.get(video_page)
    # async with browser.bidi_connection() as session:
    #     log = Log(browser, session)
    #     async with log.add_listener(Console.ALL) as messages:
    #         browser.execute_script("console.log('I love cheese')")
    #     print(messages["message"])