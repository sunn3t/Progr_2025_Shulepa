import pandas as pd
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs, unquote_plus
import datetime

airlines_df = pd.read_excel('flights.xlsx', sheet_name='Авіакомпанії', index_col='Id')
airports_df = pd.read_excel('flights.xlsx', sheet_name='Аеропорти', index_col='Id')
flights_df = pd.read_excel('flights.xlsx', sheet_name='Рейси')


def application(environ, start_response):
    params = parse_qs(environ.get('QUERY_STRING', ''))
    path = environ.get('PATH_INFO', '/')
    response_html = []

    def render_header():
        return ('<html><head><meta charset="utf-8"><title>Flight Search WSGI</title></head>'
                '<body><h1>Пошук рейсів</h1>')

    def render_footer():
        return '</body></html>'

    if 'from_id' not in params or 'to_id' not in params or 'date' not in params:
        html = render_header()
        html += '<form method="get">'
        html += '<label>Відправлення:&nbsp;'
        html += '<select name="from_id">'
        for code, row in airports_df.iterrows():
            html += f'<option value="{code}">{code} – {row.Airport} ({row.City})</option>'
        html += '</select></label><br><br>'
        html += '<label>Прибуття:&nbsp;'
        html += '<select name="to_id">'
        for code, row in airports_df.iterrows():
            html += f'<option value="{code}">{code} – {row.Airport} ({row.City})</option>'
        html += '</select></label><br><br>'
        html += '<label>Дата (YYYY-MM-DD):&nbsp;'
        html += '<input type="date" name="date" required></label><br><br>'
        html += '<button type="submit">Показати рейси</button>'
        html += '</form>'
        html += render_footer()
        response_html = html
    else:
        from_id = params['from_id'][0]
        to_id = params['to_id'][0]
        date_str = params['date'][0]
        try:
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            weekday = date_obj.isoweekday()  # 1=Mon, 7=Sun
        except ValueError:
            response_html = render_header() + f'<p>Неправильний формат дати: {date_str}</p>' + render_footer()
            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
            return [response_html.encode('utf-8')]

        sel = flights_df[
            (flights_df.from_id == from_id) &
            (flights_df.to_id == to_id)
        ]
        html = render_header()
        html += f'<p>Рейси з {from_id} до {to_id} на {date_str}:</p>'

        available = []
        for idx, flight in sel.iterrows():
            days = str(flight.Days)
            if len(days) >= weekday and days[weekday-1] != '0':
                available.append(flight)

        if not available:
            html += '<p>Немає доступних рейсів.</p>'
            html += '<p><a href="/">Повернутися</a></p>'
        else:
            if 'chosen' not in params:
                html += '<form method="get">'
                html += f'<input type="hidden" name="from_id" value="{from_id}">'
                html += f'<input type="hidden" name="to_id" value="{to_id}">'
                html += f'<input type="hidden" name="date" value="{date_str}">'
                html += '<table border="1" cellpadding="5">'
                html += ('<tr><th>Вибір</th><th>Рейс</th><th>Авіакомпанія</th>'
                         '<th>Відправлення</th><th>Прибуття</th><th>Клас</th><th>Вартість</th></tr>')
                for i, flight in enumerate(available):
                    airline = airlines_df.loc[flight.Class if False else flight.Flight[:2], 'Name'] if False else airlines_df.loc[flight.Flight[:2], 'Name']
                    html += ('<tr>'
                             f'<td><input type="radio" name="chosen" value="{i}" required></td>'
                             f'<td>{flight.Flight}</td>'
                             f'<td>{airline}</td>'
                             f'<td>{flight.Depart}</td>'
                             f'<td>{flight.Arrive}</td>'
                             f'<td>{flight.Class}</td>'
                             f'<td>{flight.Cost}</td>'
                             '</tr>')
                html += '</table><br>'
                html += '<button type="submit">Підтвердити вибір</button>'
                html += '</form>'
            else:
                choice = int(params['chosen'][0])
                flight = available[choice]
                airline = airlines_df.loc[flight.Flight[:2], 'Name']
                html += '<h2>Ви обрали рейс:</h2>'
                html += '<ul>'
                html += f'<li>Номер: {flight.Flight}</li>'
                html += f'<li>Авіакомпанія: {airline}</li>'
                html += f'<li>Час відправлення: {flight.Depart}</li>'
                html += f'<li>Час прибуття: {flight.Arrive}</li>'
                html += f'<li>Клас: {flight.Class}</li>'
                html += f'<li>Вартість: {flight.Cost}</li>'
                html += '</ul>'
                html += '<p><a href="/">Повернутися до пошуку</a></p>'
        html += render_footer()
        response_html = html

    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [response_html.encode('utf-8')]


if __name__ == '__main__':
    port = 8000
    print(f"Запуск WSGI-сервера на порту {port}...")
    with make_server('', port, application) as httpd:
        print("Сервер запущено, натисніть Ctrl+C для зупинки.")
        httpd.serve_forever()
