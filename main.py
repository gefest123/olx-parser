import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import helpers
import json



def get_pages(page):
    req = requests.get(page)
    soup = BeautifulSoup(req.text, 'html.parser')
    pages = soup.find('ul',{'data-testid':'pagination-list'}).findAll('li')[-1].getText()
    return int(pages)


def get_data(response):
    soup = BeautifulSoup(response, 'html.parser')
    all_ads = soup.findAll("div", {'data-cy': 'l-card'})
    for ads in all_ads:
        with open('ads.txt', 'a') as f:
            f.write(f'https://www.olx.ua{ads.find("a")["href"]}\n')

# Function to fetch data from server
def fetch(session, base_url):
    with session.get(base_url) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(base_url))
        return data


async def get_data_asynchronous(start_page):
    start_page = helpers.cleanUrl(start_page)
    pages = get_pages(start_page)
    print(pages)
    urls = [f'{start_page}?page={i}' for i in range(pages + 1)]
    with ThreadPoolExecutor(max_workers=20) as executor:
        with requests.Session() as session:
            # Set any session parameters here before calling `fetch`
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, url)  # Allows us to pass in multiple arguments to `fetch`
                )
                for url in urls
            ]
            for response in await asyncio.gather(*tasks):
                get_data(response)


def main(page):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(get_data_asynchronous(page))
    except KeyboardInterrupt:
        pass

page = helpers.cleanUrl(input('Enter the section example: "https://www.olx.ua/d/uk/transport/gruzovye-avtomobili/"'))
main(page)