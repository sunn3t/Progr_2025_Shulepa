import json
import os
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs, unquote_plus
import datetime


CUSTOMERS_FILE = 'customers.json'
PRODUCTS_FILE = 'products.json'
INVOICES_FILE = 'invoices.json'
ITEMS_FILE = 'items.json'

for filename in (CUSTOMERS_FILE, PRODUCTS_FILE, INVOICES_FILE, ITEMS_FILE):
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)


def load_json(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(fn, data):
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def next_id(prefix, items):
    nums = [int(item['id'][len(prefix):]) for item in items if item['id'].startswith(prefix)]
    n = max(nums) + 1 if nums else 1
    return f"{prefix}{n:03d}"


def render_header(title):
    return (f'<html><head><meta charset="utf-8"><title>{title}</title></head>'
            '<body>')

def render_footer():
    return '</body></html>'


def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    params = parse_qs(environ.get('QUERY_STRING', ''), keep_blank_values=True)

    customers = load_json(CUSTOMERS_FILE)
    products = load_json(PRODUCTS_FILE)
    invoices = load_json(INVOICES_FILE)
    items = load_json(ITEMS_FILE)

    if path == '/invoices':
        if 'client_id' in params:
            client_id = params['client_id'][0]
            inv_id = next_id('I', invoices)
            number = params.get('number', [''])[0] or inv_id
            date = params.get('date', [''])[0] or datetime.date.today().isoformat()
            invoices.append({'id': inv_id, 'number': number, 'date': date, 'client': client_id})
            save_json(INVOICES_FILE, invoices)
        html = [render_header('Список рахунків'), '<h1>Рахунки</h1>']
        html.append('<table border="1" cellpadding="5"><tr><th>ID</th><th>Номер</th><th>Дата</th><th>Клієнт</th><th>Дії</th></tr>')
        for inv in invoices:
            client = next((c for c in customers if c['id']==inv['client']), {})
            name = client.get('name','')
            html.append(
                f"<tr><td>{inv['id']}</td><td>{inv['number']}</td><td>{inv['date']}</td>"
                f"<td>{name}</td>"
                f"<td><a href='/invoice/items?invoice_id={inv['id']}'>Пункти</a></td></tr>"
            )
        html.append('</table>')
        html.append('<h2>Додати рахунок</h2>')
        html.append('<form method="get">')
        html.append('Клієнт: <select name="client_id">')
        for c in customers:
            html.append(f"<option value='{c['id']}'>{c['name']}</option>")
        html.append('</select><br><br>')
        html.append('Номер: <input name="number"><br><br>')
        html.append('Дата: <input type="date" name="date"><br><br>')
        html.append('<button type="submit">Додати</button>')
        html.append('</form>')
        html.append(render_footer())
        start_response('200 OK', [('Content-Type','text/html; charset=utf-8')])
        return ['\n'.join(html).encode('utf-8')]


  if path == '/invoice/items':
        inv_id = params.get('invoice_id',[''])[0]
        invoice = next((inv for inv in invoices if inv['id']==inv_id), None)
        if not invoice:
            start_response('404 Not Found', [('Content-Type','text/plain')])
            return [b'Invoice not found']
        if 'product_id' in params and 'quantity' in params:
            prod_id = params['product_id'][0]
            try:
                qty = float(params['quantity'][0])
            except ValueError:
                qty = 0
            item_id = next_id('X', items)
            items.append({'id': item_id, 'invoice': inv_id, 'product': prod_id, 'quantity': qty})
            save_json(ITEMS_FILE, items)
         if 'delete_id' in params:
            del_id = params['delete_id'][0]
            items = [it for it in items if it['id']!=del_id]
            save_json(ITEMS_FILE, items)
        my_items = [it for it in items if it['invoice']==inv_id]
        html = [render_header(f"Пункти {inv_id}"), f"<h1>Пункти рахунку {inv_id}</h1>"]
        html.append('<table border="1" cellpadding="5"><tr><th>ID</th><th>Товар</th><th>К-сть</th><th>Ціна</th><th>Сума</th><th>Дії</th></tr>')
        total = 0
        for it in my_items:
            prod = next((p for p in products if p['id']==it['product']), {})
            price = prod.get('price',0)
            subtotal = price * it['quantity']
            total += subtotal
            html.append(
                f"<tr><td>{it['id']}</td><td>{prod.get('name','')}</td><td>{it['quantity']}</td>"
                f"<td>{price}</td><td>{subtotal:.2f}</td>"
                f"<td><a href='/invoice/items?invoice_id={inv_id}&delete_id={it['id']}'>Видалити</a></td></tr>"
            )
        html.append(f"<tr><td colspan=4 align='right'><b>Всього:</b></td><td colspan=2><b>{total:.2f}</b></td></tr>")
        html.append('</table>')
        html.append('<h2>Додати пункт</h2>')
        html.append(f'<form method="get"><input type="hidden" name="invoice_id" value="{inv_id}">')
        html.append('Товар: <select name="product_id">')
        for p in products:
            html.append(f"<option value='{p['id']}'>{p['name']}</option>")
        html.append('</select><br><br>')
        html.append('Кількість: <input name="quantity" required><br><br>')
        html.append('<button type="submit">Додати</button>')
        html.append('</form>')
        html.append(f'<p><a href="/invoices">До списку рахунків</a></p>')
        html.append(render_footer())
        start_response('200 OK', [('Content-Type','text/html; charset=utf-8')])
        return ['\n'.join(html).encode('utf-8')]

    start_response('302 Found', [('Location','/invoices')])
    return [b'']

if __name__ == '__main__':
    port = 8080
    print(f"Запуск на порту {port}...")
    with make_server('', port, application) as httpd:
        print("Перейдіть у браузері: http://localhost:8080/invoices")
        httpd.serve_forever()
