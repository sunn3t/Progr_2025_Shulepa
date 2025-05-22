import os
import re
import argparse
from urllib.parse import urljoin
import requests
from html.parser import HTMLParser

BASE_URL = 'https://github.com/krenevych/informatics'
RAW_BASE = 'https://raw.githubusercontent.com/krenevych/informatics/main'
INDEX_PATH = '/tree/main'


def find_folder_regex(topic_num):
    """
    Шукає назву папки теми T{num}-[name] на сторінці індексу за допомогою regex.
    """
    idx_url = BASE_URL + INDEX_PATH
    r = requests.get(idx_url)
    r.raise_for_status()
    html = r.text

    pattern = re.compile(r'href=["\'](?P<path>/krenevych/informatics/tree/main/(T' + 
                         rf'{topic_num}-[^"\']+))["\']')
    m = pattern.search(html)
    if not m:
        raise ValueError(f"Папку T{topic_num}-... не знайдено на {idx_url}")
    return m.group('path').split('/')[-1]  # повертає T{num}-name


def download_files_regex(topic_num, out_dir):
    """
    a) Регекс для пошуку та завантаження .py, .pyw, .pdf
    """
    folder = find_folder_regex(topic_num)
    page_url = f"{BASE_URL}/tree/main/{folder}"
    r = requests.get(page_url)
    r.raise_for_status()
    html = r.text

    # шукає посилання на файли у вигляді blob
    pat = re.compile(r'href=["\'](?P<blob>/krenevych/informatics/blob/main/' + folder + r'/[^"\']+\.(?:py|pyw|pdf))["\']')
    matches = pat.finditer(html)

    os.makedirs(out_dir, exist_ok=True)
    for m in matches:
        blob_path = m.group('blob')
        # переводимо в raw посилання
        raw_path = blob_path.replace('/blob', '')
        file_url = 'https://raw.githubusercontent.com' + raw_path
        fname = os.path.basename(raw_path)
        dest = os.path.join(out_dir, fname)
        print(f"Downloading {file_url} -> {dest}")
        rr = requests.get(file_url)
        rr.raise_for_status()
        with open(dest, 'wb') as f:
            f.write(rr.content)
    print('Завантаження завершено (regex).')


class FolderParser(HTMLParser):
    """
    Парсер для пошуку папки теми на індексній сторінці.
    """
    def __init__(self, topic_num):
        super().__init__()
        self.topic_num = str(topic_num)
        self.folder = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a' and self.folder is None:
            for attr, val in attrs:
                if attr == 'href' and f'/tree/main/T{self.topic_num}-' in val:
                    self.folder = val.split('/')[-1]


class FileParser(HTMLParser):
    """
    Парсер для пошуку файлів у папці теми.
    """
    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        self.files = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for attr, val in attrs:
                if attr == 'href' and f'/blob/main/{self.folder}/' in val:
                    if val.lower().endswith(('.py', '.pyw', '.pdf')):
                        self.files.append(val)


def download_files_parser(topic_num, out_dir):
    """
    b) HTMLParser для структурного аналізу індексу та сторінки теми.
    """
    # Індекс
    idx_url = BASE_URL + INDEX_PATH
    r = requests.get(idx_url)
    r.raise_for_status()
    parser1 = FolderParser(topic_num)
    parser1.feed(r.text)
    if not parser1.folder:
        raise ValueError(f"Папку T{topic_num}-... не знайдено на {idx_url}")

    # Сторінка теми
    topic_url = f"{BASE_URL}/tree/main/{parser1.folder}"
    rr = requests.get(topic_url)
    rr.raise_for_status()
    parser2 = FileParser(parser1.folder)
    parser2.feed(rr.text)

    os.makedirs(out_dir, exist_ok=True)
    for blob in set(parser2.files):
        raw_path = blob.replace('/blob', '').replace('github.com/krenevych/informatics', '')
        file_url = RAW_BASE + raw_path
        fname = os.path.basename(raw_path)
        dest = os.path.join(out_dir, fname)
        print(f"Downloading {file_url} -> {dest}")
        resp = requests.get(file_url)
        resp.raise_for_status()
        with open(dest, 'wb') as f:
            f.write(resp.content)
    print('Завантаження завершено (parser).')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Завантажує матеріали теми курсу з GitHub')
    p.add_argument('topic', type=int, help='Номер теми, наприклад 26')
    p.add_argument('out_dir', help='Директорія для збереження матеріалів')
    p.add_argument('--method', choices=['regex', 'parser'], default='regex',
                   help='Метод парсингу: regex або parser')
    args = p.parse_args()

    if args.method == 'regex':
        download_files_regex(args.topic, args.out_dir)
    else:
        download_files_parser(args.topic, args.out_dir)
