import json
import re
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs


def find_longest_run(s: str):
    if not s:
        return None, 0
    max_char = s[0]
    max_len = 1
    curr_char = s[0]
    curr_len = 1
    for c in s[1:]:
        if c == curr_char:
            curr_len += 1
        else:
            if curr_len > max_len:
                max_len = curr_len
                max_char = curr_char
            curr_char = c
            curr_len = 1
    if curr_len > max_len:
        max_len = curr_len
        max_char = curr_char
    return max_char, max_len


def application(environ, start_response):
    params = parse_qs(environ.get('QUERY_STRING', ''), keep_blank_values=True)
    text = params.get('text', [''])[0]
    fmt = params.get('format', ['json'])[0].lower()

    if 'text' not in params:
        html = ['<html><head><meta charset="utf-8"><title>Longest Run</title></head><body>']
        html.append('<h1>Введіть рядок</h1>')
        html.append('<form method="get">')
        html.append('<textarea name="text" rows="4" cols="50"></textarea><br><br>')
        html.append('Формат: ') 
        html.append('<select name="format">')
        html.append('<option value="json">JSON</option>')
        html.append('<option value="xml">XML</option>')
        html.append('</select><br><br>')
        html.append('<button type="submit">Надіслати</button>')
        html.append('</form></body></html>')
        body = '\n'.join(html)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [body.encode('utf-8')]

    char, length = find_longest_run(text)
    if length == 0:
        result_json = {"char": None, "length": 0}
    else:
        result_json = {"char": char, "length": length}

    if fmt == 'xml':
        xml = ['<?xml version="1.0" encoding="utf-8"?>', '<result>']
        xml.append(f'  <char>{char if char is not None else ""}</char>')
        xml.append(f'  <length>{length}</length>')
        xml.append('</result>')
        body = '\n'.join(xml)
        content_type = 'application/xml; charset=utf-8'
    else:
        body = json.dumps(result_json, ensure_ascii=False, indent=2)
        content_type = 'application/json; charset=utf-8'

    start_response('200 OK', [('Content-Type', content_type)])
    return [body.encode('utf-8')]

if __name__ == '__main__':
    port = 8080
    print(f"Запуск WSGI-сервера на порту {port}...")
    with make_server('', port, application) as httpd:
        print("Сервер запущено. Перейдіть у браузері за адресою http://localhost:8080/ ")
        httpd.serve_forever()
