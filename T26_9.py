import requests
import re
from html.parser import HTMLParser
from urllib.parse import urljoin

# Встановіть кількість сторінок для аналізу та ім'я колонки автора
BASE_URL = 'http://www.pravda.com.ua/columns/page_{}/'
AUTHOR = 'Імʼя автора'
START_PAGE = 1
END_PAGE = 5  # змініть за потреби

# Словники позитивних та негативних слів
POSITIVE_WORDS = {'добро', 'успіх', 'перемога', 'радість', 'підтримка'}
NEGATIVE_WORDS = {'провал', 'проблема', 'криза', 'сум', 'конфлікт'}

