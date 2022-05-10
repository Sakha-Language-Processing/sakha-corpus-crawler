import scrapy
from bs4 import BeautifulSoup

BASE_URL = 'http://kyym.ru'


class KyymSpider(scrapy.Spider):
    name = 'kyym'
    allowed_domains = ['kyym.ru']
    start_urls = [BASE_URL + '/']

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        article = soup.find('article', class_='article')

        if article:
            # Это статья
            header = article.find('header', class_='article-header')
            main = article.find('div', class_='main-cont')
            yield {
                'url': response.url,
                'title': header.get_text().strip(),
                'text': main.get_text().strip(),
            }

        else:
            # Это раздел
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('/'):
                    href = BASE_URL + href
                    yield scrapy.Request(url=href, callback=self.parse)
