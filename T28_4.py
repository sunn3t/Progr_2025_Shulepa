import json
import os
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs, unquote_plus

TOYS_FILE = 'toys.json'

if not os.path.exists(TOYS_FILE):
    with open(TOYS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False)


def load_toys():
    with open(TOYS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_toys(toys):
    with open(TOYS_FILE, 'w', encoding='utf-8') as f:
        json.dump(toys, f, ensure_ascii=False, indent=2)


def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    params = parse_qs(environ.get('QUERY_STRING', ''), keep_blank_values=True)

    if path == '/input':
        if 'name' in params and 'cost' in params and 'min_age' in params and 'max_age' in params:
            name = unquote_plus(params['name'][0])
            try:
                cost = float(params['cost'][0])
                min_age = int(params['min_age'][0])
                max_age = int(params['max_age'][0])
            except ValueError:
                status = '400 Bad Request'
                body = '<p>Некоректні вхідні дані</p>'
                start_response(status, [('Content-Type', 'text/html; charset=utf-8')])
                return [body.encode('utf-8')]
            toys = load_toys()
            toys.append({
                'name': name,
                'cost': cost,
                'min_age': min_age,
                'max_age': max_age
            })
            save_toys(toys)
            body = ('<html><body>'
                    '<p>Іграшку додано!</p>'
                    '<p><a href="/input">Додати ще</a> | '
                    '<a href="/filter">Перейти до фільтрів</a></p>'
                    '</body></html>')
            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
            return [body.encode('utf-8')]

      html = ['<html><head><meta charset="utf-8"><title>Додати іграшку</title></head><body>']
        html.append('<h1>Введіть відомості про іграшку</h1>')
        html.append('<form method="get">')
        html.append('Назва: <input name="name" required><br><br>')
        html.append('Вартість (грн): <input name="cost" required><br><br>')
        html.append('Вік від: <input name="min_age" required><br><br>')
        html.append('Вік до: <input name="max_age" required><br><br>')
        html.append('<button type="submit">Додати</button>')
        html.append('</form></body></html>')
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return ['\n'.join(html).encode('utf-8')]

    if path == '/filter':
        if 'age' in params or 'max_cost' in params:
            toys = load_toys()
            age = None
            max_cost = None
            try:
                if 'age' in params and params['age'][0]:
                    age = int(params['age'][0])
                if 'max_cost' in params and params['max_cost'][0]:
                    max_cost = float(params['max_cost'][0])
            except ValueError:
                age = None
                max_cost = None
            filtered = []
            for toy in toys:
                ok = True
                if age is not None:
                    ok &= (toy['min_age'] <= age <= toy['max_age'])
                if max_cost is not None:
                    ok &= (toy['cost'] <= max_cost)
                if ok:
                    filtered.append(toy)
            body = json.dumps({'toys': filtered}, ensure_ascii=False, indent=2)
            start_response('200 OK', [('Content-Type', 'application/json; charset=utf-8')])
            return [body.encode('utf-8')]
        html = ['<html><head><meta charset="utf-8"><title>Фільтр іграшок</title></head><body>']
        html.append('<h1>Фільтрувати іграшки</h1>')
        html.append('<form method="get">')
        html.append('Вік дитини: <input name="age"><br><br>')
        html.append('Макс. вартість (грн): <input name="max_cost"><br><br>')
        html.append('<button type="submit">Застосувати</button>')
        html.append('</form>')
        html.append('<p><a href="/input">Додати іграшки</a></p>')
        html.append('</body></html>')
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return ['\n'.join(html).encode('utf-8')]

    start_response('302 Found', [('Location', '/input')])
    return [b'']

if __name__ == '__main__':
    port = 8080
    print(f"Запуск сервера на порту {port}...")
    with make_server('', port, application) as httpd:
        print("Відкрийте http://localhost:8080/input для початку.")
        httpd.serve_forever()
