from requests import Session
from bs4 import BeautifulSoup as bs
from time import sleep
import os


PAGE_COUNT=1
PAUSE = 2
DOWNLOAD_FOLDER = 'img'
BASE_URL = 'https://quotes.toscrape.com/'
headers = \
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}


def write_data(text, author):
    with open('data.txt', 'a', encoding='utf-8') as f:
        f.write(f'{text}\n Автор: {author}\n' + '*'*20 + '\n')



session = Session()
session.get(BASE_URL, headers=headers)
response = session.get(BASE_URL+"login", headers=headers)
soup = bs(response.text, "lxml")
token = soup.find("form").find("input").get("value")
print(token)

post_data = {'username': 'sa', 'password': '123', 'csrf_token': token}
result = session.post(BASE_URL + "login", headers=headers, data=post_data, allow_redirects=True)
page_counter = 1
while True:
    response = session.get(f"{BASE_URL}page/{page_counter}/")
    if response.status_code != 200:
        break
    soup = bs(response.text, "lxml")
    texts = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")
    if len(texts) == 0 or len(authors) == 0:
        break

    for index, author in enumerate(authors):
        write_data(texts[index].text, author.text)
    page_counter += 1


