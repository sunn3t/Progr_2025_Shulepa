import os
import re
import argparse
from urllib.parse import urljoin

import requests
from html.parser import HTMLParser

BASE_URL = 'http://matfiz.univ.kiev.ua'
TOPICS_INDEX = '/pages/13'


def download_with_regex(topic_number, out_dir):
    """
    a) Використання регулярних виразів для знаходження та завантаження прикладів .py/.pyw
    """
    # URL сторінки теми
    topic_url = urljoin(BASE_URL, f'/pages/{topic_number}')
    resp = requests.get(topic_url)
    resp.raise_for_status()
    html = resp.text

    # Шаблон для пошуку посилань на файли прикладів
    pattern = re.compile(r'href=["\'](?P<path>/userfiles/files/[^"\']+\.(?:py|pyw))["\']', re.IGNORECASE)
    matches = pattern.finditer(html)

    os.makedirs(out_dir, exist_ok=True)
    for m in matches:
        rel_path = m.group('path')
        file_url = urljoin(BASE_URL, rel_path)
        filename = os.path.basename(rel_path)
        dest = os.path.join(out_dir, filename)
        print(f'Downloading {file_url} -> {dest}')
        r = requests.get(file_url)
        r.raise_for_status()
        with open(dest, 'wb') as f:
            f.write(r.content)
    print('Done with regex method.')


class ExampleParser(HTMLParser):
    """
    HTMLParser для пошуку прикладів .py/.pyw
    """
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for attr, val in attrs:
                if attr.lower() == 'href' and val.startswith('/userfiles/files/') and val.lower().endswith(('.py', '.pyw')):
                    self.links.append(val)


def download_with_parser(topic_number, out_dir):
    """
    b) Використання HTMLParser для структурного аналізу HTML
    """
    topic_url = urljoin(BASE_URL, f'/pages/{topic_number}')
    resp = requests.get(topic_url)
    resp.raise_for_status()
    html = resp.text

    parser = ExampleParser()
    parser.feed(html)

    os.makedirs(out_dir, exist_ok=True)
    for rel_path in set(parser.links):  # унікалізуємо
        file_url = urljoin(BASE_URL, rel_path)
        filename = os.path.basename(rel_path)
        dest = os.path.join(out_dir, filename)
        print(f'Downloading {file_url} -> {dest}')
        r = requests.get(file_url)
        r.raise_for_status()
        with open(dest, 'wb') as f:
            f.write(r.content)
    print('Done with parser method.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Завантажує приклади програм із заданої теми кафедри математичної фізики.'
    )
    parser.add_argument('topic', type=int, help='Номер теми (YY)')
    parser.add_argument('out_dir', help='Каталог для збереження файлів')
    parser.add_argument('--method', choices=['regex', 'parser'], default='regex',
                        help='Метод парсингу: regex або parser')
    args = parser.parse_args()

    if args.method == 'regex':
        download_with_regex(args.topic, args.out_dir)
    else:
        download_with_parser(args.topic, args.out_dir)
