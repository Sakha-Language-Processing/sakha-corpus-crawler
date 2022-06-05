import re
from urllib.parse import unquote
import scrapy
from bs4 import BeautifulSoup

HOSTNAME = 'sah.wikipedia.org'
RE_CATEGORY = re.compile(r'\[\[Категория: .+?\]\]')
RE_CITE = re.compile(r'\[\d+\]')
RE_URL = re.compile(
    r'(https?):\/\/'  # Схема
    r'([0-9a-zA-Z.-]+)'  # Хост
    r'(:[1-9]\d+)?'  # Порт
    r'(\/[\w%.\-+]+)*\/?'  # Ресурс
    r'(\?[\w%.\-+=]+(&[\w%.\-+=]+)*)?'  # Запрос
)


def get_absolute_url(page_name: str) -> str:
    return f'https://{HOSTNAME}/w/rest.php/v1/page/{page_name}/html'


class WikiSpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = [HOSTNAME]
    main_page = 'Сүрүн_сирэй'
    start_urls = [get_absolute_url(main_page)]

    def parse(self, response):
        url = unquote(response.url)
        soup = BeautifulSoup(response.body, 'html.parser')

        # Извлекаем ссылки для дальнейшего парсинга
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('./'):
                if href.find(':') > 0:
                    continue
                if href.find('#') > 0:
                    continue
                href = get_absolute_url(href[2:])
                yield scrapy.Request(url=href, callback=self.parse)

        # Заголовок
        title = soup.find('html').find('head').find('title').text

        # Текст страницы
        paragraphs = []
        for section in soup.find_all('section'):
            for para in section.find_all('p', recursive=False):
                # Убираем двойные пробелы и разрывы строк
                text = ' '.join(para.get_text().split())
                # Убираем ссылки на категорию
                text = re.sub(RE_CATEGORY, '', text)
                # Убираем ссылки на источники
                text = re.sub(RE_CITE, '', text)
                # Убираем URL-ы
                text = re.sub(RE_URL, '', text)
                # Добавляем параграф
                if text:
                    paragraphs.append(text)

        yield {
            'url': url,
            'title': title,
            'text': ' '.join(paragraphs),
        }
