import json
import re
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

WORD_PATTERN = re.compile(r"\b[\w']+\b", re.UNICODE)

def application(environ, start_response):
    params = parse_qs(environ.get('QUERY_STRING', ''), keep_blank_values=True)
    text = params.get('text', [''])[0]
    fmt = params.get('format', ['json'])[0].lower()

    words = WORD_PATTERN.findall(text)
    distinct = sorted({w.lower() for w in words if w.strip()})

    if fmt == 'xml':
        root = ['<?xml version="1.0" encoding="utf-8"?>', '<words>']
        for w in distinct:
            root.append(f'  <word>{w}</word>')
        root.append('</words>')
        body = '\n'.join(root)
        content_type = 'application/xml; charset=utf-8'
    else:
        data = {'words': distinct}
        body = json.dumps(data, ensure_ascii=False, indent=2)
        content_type = 'application/json; charset=utf-8'

    start_response('200 OK', [('Content-Type', content_type)])
    return [body.encode('utf-8')]

if __name__ == '__main__':
    port = 8080
    print(f"Запуск сервера на порту {port}...")
    with make_server('', port, application) as httpd:
        print("Сервер запущено, перейдіть за адресою http://localhost:8080/?text=+&format=json")
        httpd.serve_forever()
