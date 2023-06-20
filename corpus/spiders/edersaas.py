from datetime import datetime

import scrapy
from bs4 import BeautifulSoup

DOMAIN = 'edersaas.ru'
SPLITTER = ' Оцени: '


class EdersaasSpider(scrapy.Spider):
    name = "edersaas"
    allowed_domains = [DOMAIN]
    start_urls = [f"https://{DOMAIN}"]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        article = soup.find('article', class_='post')
        quiz = soup.find('div', class_='wq-quiz')

        if article and not quiz:
            # Это статья
            header = article.find('h1', class_='dmi-news-title')
            main = article.find('div', id='content')
            published_tag = soup.find('meta', property='article:published_time')
            try:
                published_str = published_tag.attrs['content']
                published = datetime.strptime(published_str, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                published = datetime(1970, 1, 1)

            text = main.get_text()
            text = text.replace('­', ' ')
            text, _ = text.split(SPLITTER)
            text = ' '.join(text.split())

            yield {
                'url': response.url,
                'published': published.timestamp(),
                'title': header.get_text().strip(),
                'text': text,
            }

        # Ссылки на странице
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith(f'https://{DOMAIN}/'):
                yield scrapy.Request(url=href, callback=self.parse)
