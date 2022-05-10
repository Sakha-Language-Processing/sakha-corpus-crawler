import scrapy
from bs4 import BeautifulSoup


class WikiSpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['sah.wikipedia.org']
    start_urls = ['https://sah.wikipedia.org/']

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
