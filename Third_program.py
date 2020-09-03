import requests
import bs4
from collections import namedtuple

COMFORTABLE_FORMAT = namedtuple('FORMAT', 'title,city,price,url')

class FORMAT(COMFORTABLE_FORMAT):
    def __str__(self):
        return f'{self.title}\t\t {self.city}\t\t {self.price}\t {self.url}'

class OlxParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }


    def get_page(self, page: int = None):
        params = {}
        if page and page < 0:
            page = 1

        if page and page > 1:
            params['p'] = page

        url = 'https://www.olx.kz/elektronika/telefony-i-aksesuary/'
        r = self.session.get(url, params = params)

        return r.text

    def parse_block(self, item):
        #ССЫЛКА
        url_block = item.select_one('a.marginright5.link.linkWithHash.detailsLink')
        url = url_block.get('href')

        #названия
        title = item.select_one('h3.lheight22.margintop5 strong')
        title = title.string.strip()

        #Город
        city = item.select_one('small.breadcrumb.x-normal span' )
        city = city.text

        #Цена
        price = item.select_one('p.price strong')
        price = price.string
        return FORMAT(title = title, city = city, price = price, url = url)



    def get_block(self, n):
        text = self.get_page(page = n)
        soup = bs4.BeautifulSoup(text, 'lxml')
        block_top = soup.find_all("table", class_ = "fixed offers breakword offers--top redesigned")
        block_usual = soup.find_all("table", {'summary': 'Объявления'})

        block_top_wrap = bs4.BeautifulSoup(str(block_top), "lxml" )
        block_top_wrap = block_top_wrap.find_all("tr", class_ = "wrap")

        block_usual_wrap = bs4.BeautifulSoup(str(block_usual), "lxml")
        block_usual_wrap = block_usual_wrap.find_all("tr", class_="wrap")

        for item in block_usual_wrap:
            block = self.parse_block(item=item)
            print(block)


p = OlxParser()

page = int(input("Введите страницу: "))
p.get_block(page)