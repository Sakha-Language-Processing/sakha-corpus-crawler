from urllib.parse import unquote
import scrapy
from bs4 import BeautifulSoup

BASE_URL = 'https://sah.wikipedia.org'


class WikiSpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['sah.wikipedia.org']
    start_urls = [BASE_URL + '/']

    def parse(self, response):
        url = unquote(response.url)
        soup = BeautifulSoup(response.body, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/wiki/'):
                href = BASE_URL + href
                yield scrapy.Request(url=href, callback=self.parse)

        # Пропускаем специальные страницы
        if url.count(':') > 1:
            return None

        content = soup.find('div', id='content')
        head_tag = content.find(id='firstHeading')
        text_tag = content.find(id='mw-content-text')
        if head_tag and text_tag:
            yield {
                'url': url,
                'title': head_tag.get_text().strip(),
                'text': text_tag.get_text().strip(),
            }
