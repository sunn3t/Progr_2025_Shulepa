import sqlite3
import os
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs, quote_plus

DB_FILE = 'project.db'

# Ініціалізація БД
def init_db():
    first_time = not os.path.exists(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    if first_time:
        c = conn.cursor()
        # Сайти
        c.execute('''
            CREATE TABLE sites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                address TEXT,
                resp_customer TEXT,
                resp_contractor TEXT
            )''')
        # Роботи
        c.execute('''
            CREATE TABLE works (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL
            )''')
        # Акти
        c.execute('''
            CREATE TABLE acts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL,
                date TEXT NOT NULL,
                sum REAL,
                site_id INTEGER NOT NULL,
                FOREIGN KEY(site_id) REFERENCES sites(id)
            )''')
        # Пункти акту
        c.execute('''
            CREATE TABLE items (
                act_id INTEGER NOT NULL,
                work_id INTEGER NOT NULL,
                FOREIGN KEY(act_id) REFERENCES acts(id),
                FOREIGN KEY(work_id) REFERENCES works(id)
            )''')
        conn.commit()
    return conn

# HTML-шаблони

def render_header(title):
    return f'<html><head><meta charset="utf-8"><title>{title}</title></head><body><h1>{title}</h1>'

def render_footer():
    return '</body></html>'

# WSGI-додаток

def application(environ, start_response):
    conn = init_db()
    c = conn.cursor()
    params = parse_qs(environ.get('QUERY_STRING',''))
    html = ''
    # Вибір майданчику
    if 'site_id' not in params:
        title = 'Вибір майданчику'
        html = render_header(title)
        c.execute('SELECT id, name FROM sites')
        sites = c.fetchall()
        html += '<form method="get">'
        html += '<label>Майданчик: <select name="site_id">'
        for sid, name in sites:
            html += f'<option value="{sid}">{name}</option>'
        html += '</select></label><br><br>'
        html += '<button type="submit">Показати перелік робіт</button>'
        html += '</form>'
    else:
        # Перелік робіт для обраного майданчику
        site_id = int(params['site_id'][0])
        # Отримуємо назву майданчику
        c.execute('SELECT name FROM sites WHERE id = ?', (site_id,))
        row = c.fetchone()
        site_name = row[0] if row else '---'
        title = f'Перелік робіт для майданчику "{site_name}"'
        html = render_header(title)
        # Знаходимо всі акти цього майданчику
        c.execute('SELECT id, number, date, sum FROM acts WHERE site_id = ?', (site_id,))
        acts = c.fetchall()
        if not acts:
            html += '<p>Немає сформованих актів.</p>'
        else:
            for aid, number, date, total in acts:
                html += f'<h2>Акт №{number} від {date} — Сума: {total}</h2>'
                # Знаходимо пункти акту
                c.execute('''
                    SELECT w.code, w.name
                    FROM items i
                    JOIN works w ON i.work_id = w.id
                    WHERE i.act_id = ?
                ''', (aid,))
                items = c.fetchall()
                if items:
                    html += '<ul>'
                    for code, name in items:
                        html += f'<li>{code} – {name}</li>'
                    html += '</ul>'
                else:
                    html += '<p>Немає пунктів у цьому акті.</p>'
        html += '<p><a href="/">← Назад до вибору майданчику</a></p>'
    html += render_footer()
    start_response('200 OK', [('Content-Type','text/html; charset=utf-8')])
    return [html.encode('utf-8')]

if __name__=='__main__':
    port = 8000
    print(f"Запуск WSGI-сервера на порту {port}...")
    with make_server('', port, application) as httpd:
        print("Сервер запущено. Перейдіть у браузері http://localhost:8000/")
        httpd.serve_forever()
