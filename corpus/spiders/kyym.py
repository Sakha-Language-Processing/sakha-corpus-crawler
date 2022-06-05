import scrapy
from bs4 import BeautifulSoup
from datetime import datetime

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
            published_tag = article.find('time')
            try:
                published_str = published_tag.attrs['datetime'].replace(':', '')
                published = datetime.strptime(published_str, '%Y-%m-%dT%H%M%S%z')
            except ValueError:
                published = datetime(1970, 1, 1)

            text = main.get_text()
            text = text.replace('­', ' ')
            text = text.replace('Тарҕат:', '')
            text = ' '.join(text.split())
            text = text.replace(' * * * ', ' ')

            yield {
                'url': response.url,
                'published': published.timestamp(),
                'title': header.get_text().strip(),
                'text': text,
            }

        else:
            # Это раздел
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('/'):
                    href = BASE_URL + href
                    yield scrapy.Request(url=href, callback=self.parse)
