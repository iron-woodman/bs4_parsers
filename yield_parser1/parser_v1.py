import json
import requests
from bs4 import BeautifulSoup as bs
from time import sleep


PAGE_COUNT=1
PAUSE = 2
BASE_URL = 'https://scrapingclub.com'
headers = \
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

def write_to_json(data: dict, file: str):
    """
    сохраняем результат  парсинга в файл csv
    :param data:
    :return:
    """
    with open(file, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, separators=(',', ': '))


def write_to_csv(data, file):
    with open(file, 'a', encoding='utf-8') as f:
        f.write(';'.join(data))
        f.write('\n')


def get_filename_from_sitenname(domen_name):
    name = BASE_URL.replace('https://', '')
    name = name.replace('http://','')
    name = name.split('/')[0] + ".txt"
    return name

def get_page_url():
    global PAGE_COUNT
    for page_number in range(1, PAGE_COUNT + 1):
        url = BASE_URL + f'/exercise/list_basic/?Page={page_number}'
        yield url


def get_card_url(page_url):
    print(f'\nПарсинг страницы {page_url}\n')
    response = requests.get(page_url, headers=headers)
    soup = bs(response.text, "lxml")
    cards = soup.find_all('div', class_='w-full rounded border')
    for card in cards:
        card_link = BASE_URL + card.find('a').get('href')
        yield card_link
        # print('*' * 10)


def get_card_data(card_url):
    url = card_url
    print('='*10, '\n',url)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f'{card_url} - ', response)
        return
    soup = bs(response.text, "lxml")
    card_data = soup.find('div', class_="my-8 w-full rounded border")
    title = card_data.find('h3', class_="card-title").text
    price = card_data.find('h4', class_="my-4 card-price").text
    description = card_data.find('p', class_="card-description").text
    img_link = BASE_URL + card_data.find('img').get('src')

    print(title, '\n', price, '\n', description, '\n', img_link)
    # write_to_json({'title':title, 'price': price, 'description': description, 'img':img_link}, get_filename_from_sitenname(BASE_URL))
    yield title, price, description, img_link
    sleep(PAUSE)


def main():

    page_urls = get_page_url()
    for url in page_urls:
        card_urls = get_card_url(url)
        for card_url in card_urls:
            card_data = get_card_data(card_url)
            for data in card_data:
                if data is not None:
                    print(data)
                    write_to_csv(data, get_filename_from_sitenname(BASE_URL))



if __name__ == "__main__":
    main()