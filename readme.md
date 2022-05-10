# Создание корпуса якутских текстов

## Источники

1. [Бипипиэдьийэ](https://sah.wikipedia.org/)
2. [Кыым](https://kyym.ru/)

## Инструменты

* [Python](https://python.org/)
* [Scrapy](https://scrapy.org/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

## Порядок работы

1. Установить Python
2. Склонировать репозиторий
3. Создать и активировать виртуальное окружение:

```
python -m venv venv
venv\scripts\activate.bat
```

4. Установить библиотеки:

```
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt
```

5. Запустить процесс сбора корпуса:

```
scrapy crawl wiki -O wiki.json
scrapy crawl kyym -O kyym.json
```

## Использованные примеры

* https://proxiesapi.com/blog/how-to-scrape-wikipedia-using-python-scrapy.html.php
* https://proxiesapi-com.medium.com/how-to-scrape-wikipedia-using-python-scrapy-8a867efae2ab
* https://gist.github.com/vijayanandrp/574e5da2df817ee6f20bfa937ab9b5e9
