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

def fetch_article_links(page: int) -> list:
    """За допомогою регулярних виразів витягуємо посилання на статті автора."""
    url = BASE_URL.format(page)
    resp = requests.get(url)
    resp.raise_for_status()
    text = resp.text
    # Шукаймо блок author та витягнемо href
    pattern = re.compile(r'<a[^>]*href="([^"]+)"[^>]*>[^<]*' + re.escape(AUTHOR) + r'[^<]*<')
    links = pattern.findall(text)
    return [urljoin(url, link) for link in links]


def analyze_sentiment(text: str) -> str:
    """Підрахунок позитивних та негативних слів у тексті."""
    words = re.findall(r"\b[А-Яа-яЇїЄєІі'\-]+\b", text.lower())
    pos_count = sum(w in POSITIVE_WORDS for w in words)
    neg_count = sum(w in NEGATIVE_WORDS for w in words)
    return 'Позитивна' if pos_count > neg_count else 'Негативна'


def regex_mode():
    results = []
    for page in range(START_PAGE, END_PAGE + 1):
        for link in fetch_article_links(page):
            r = requests.get(link)
            r.raise_for_status()
            sentiment = analyze_sentiment(r.text)
            results.append((link, sentiment))
    return results


class PravdaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_article = False
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        # Зазвичай контент статті в <div class="article-text"> або схоже
        if tag == 'div' and any(val == 'article-text' for (_tag, val) in attrs):
            self.in_article = True

    def handle_endtag(self, tag):
        if self.in_article and tag == 'div':
            self.in_article = False

    def handle_data(self, data):
        if self.in_article:
            self.text_parts.append(data)

    def get_text(self):
        return ' '.join(self.text_parts)


def htmlparser_mode():
    results = []
    for page in range(START_PAGE, END_PAGE + 1):
        links = fetch_article_links(page)
        for link in links:
            r = requests.get(link)
            r.raise_for_status()
            parser = PravdaParser()
            parser.feed(r.text)
            content = parser.get_text()
            sentiment = analyze_sentiment(content)
            results.append((link, sentiment))
    return results
