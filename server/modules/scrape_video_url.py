import requests
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
        
        # Video lnk example: /fr/videos/117014-031-A/arte-journal/
        # API link example: https://api.arte.tv/api/player/v2/config/fr/117014-031-A
        api_link = f'https://api.arte.tv/api/player/v2/config/fr/{video_link.replace("/fr/videos/","").split("/arte-journal")[0]}'
        response = requests.get(api_link).json()
        return response["data"]["attributes"]["streams"][0]["url"]