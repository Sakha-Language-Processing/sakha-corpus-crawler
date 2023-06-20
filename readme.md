# Создание корпуса якутских текстов

## Источники

1. [Бипипиэдьийэ](https://sah.wikipedia.org/) — более 10000 статей (более 10 мб).
2. [Кыым](https://kyym.ru/) — более 9200 статей начиная с февраля 2018 года (более 50 мб).
3. [Эдэр саас](https://edersaas.ru/) — .

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
scrapy crawl edersaas -O edersaas.json
```

Если процесс сбора нужно выполнить в несколько заходов, то можно задать параметр `JOBDIR` с помощью ключа `-s`:

```
scrapy crawl wiki -s JOBDIR=checkpoint -o wiki.json
```

При этом, для сохранения данных нужно использовать ключ `-o` (добавление) вместо `-O` (перезапись).

## Использованные примеры

* https://proxiesapi.com/blog/how-to-scrape-wikipedia-using-python-scrapy.html.php
* https://gist.github.com/vijayanandrp/574e5da2df817ee6f20bfa937ab9b5e9
