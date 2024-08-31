import pprint
import requests
import pandas as pd
from bs4 import BeautifulSoup

def parseBooks(url):
    print('**************************************** URL: ', url)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    headers = {'User-Agent': user_agent}
    page = requests.request('GET', url=url, headers=headers)
    html = page.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def getPages():
    url = 'https://books.toscrape.com/catalogue/'
    soup = parseBooks(url + "page-46.html")
    get_books_info(soup)
    nextPage = soup.select('li.next')

    while (len(nextPage)  != 0):
        link = nextPage[0].find('a')['href']
        # print('******************************************************* NextPage: ', url + link)

        soup = parseBooks(url + link)
        get_books_info(soup)
        nextPage = soup.select('li.next')

def get_books_info(soup):
    books = []

    titles = soup.select('a[title]')
    prices = soup.select('p.price_color')
    availability = soup.select('p.instock')
    rating = soup.select('p.star-rating')

    for i, title in enumerate(titles):
        books.append({'title': title['title']})
        books[i]['price'] = prices[i].text.strip('Â£')
        books[i]['available'] = availability[i].text.strip()
        books[i]['rating'] = rating[i].get("class")[1]

    # pp = pprint.PrettyPrinter(depth=4)
    # pprint.pp(books)
    df = pd.DataFrame(books)
    df.head()

if __name__ == "__main__":
    #get_books_info()
    getPages()
    print('Fim Main')


