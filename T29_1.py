import sqlite3
import datetime
import os

DB_FILE = 'birthdays.db'


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS acquaintances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            surname TEXT NOT NULL,
            name TEXT NOT NULL,
            birthdate TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

def add_acquaintance(conn):
    surname = input('Прізвище: ').strip()
    name = input("Імя:").strip()
    while True:
        bd_str = input('Дата народження (YYYY-MM-DD): ').strip()
        try:
            datetime.datetime.strptime(bd_str, '%Y-%m-%d')
            break
        except ValueError:
            print('Неправильний формат. Спробуйте ще раз.')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO acquaintances (surname, name, birthdate) VALUES (?, ?, ?)',
        (surname, name, bd_str)
    )
    conn.commit()
    print('Знайомого додано.')

def show_birthday_by_surname(conn):
    surname = input('Введіть прізвище для пошуку: ').strip()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT surname, name, birthdate FROM acquaintances WHERE surname = ?',
        (surname,)
    )
    rows = cursor.fetchall()
    if not rows:
        print('Знайомих з таким прізвищем не знайдено.')
    else:
        for sur, name, bd in rows:
            print(f"{sur} {name} — {bd}")

def show_upcoming_birthdays(conn, days_ahead=7):
    today = datetime.date.today()
    end = today + datetime.timedelta(days=days_ahead)
    cursor = conn.cursor()
    cursor.execute('SELECT surname, name, birthdate FROM acquaintances')
    rows = cursor.fetchall()
    upcoming = []
    for sur, name, bd_str in rows:
        bd = datetime.datetime.strptime(bd_str, '%Y-%m-%d').date()
      
        this_year_bd = bd.replace(year=today.year)
        if today <= this_year_bd <= end:
            days_left = (this_year_bd - today).days
            upcoming.append((sur, name, this_year_bd.isoformat(), days_left))
    if upcoming:
        print(f"Знайомі, у яких день народження за наступні {days_ahead} днів:")
        for sur, name, bd_iso, left in upcoming:
            print(f"  {sur} {name}: {bd_iso} (через {left} днів)")
    else:
        print(f"Ніхто не святкує день народження протягом наступних {days_ahead} днів.")

if __name__ == '__main__':
    conn = init_db()
    print('=== Список найближчих днів народження ===')
    show_upcoming_birthdays(conn)
    while True:
        print('\nМеню:')
        print('1. Додати знайомого')
        print('2. Показати дату народження за прізвищем')
        print('3. Вихід')
        choice = input('Ваш вибір: ').strip()
        if choice == '1':
            add_acquaintance(conn)
        elif choice == '2':
            show_birthday_by_surname(conn)
        elif choice == '3':
            print('До побачення!')
            break
        else:
            print('Невірний вибір, спробуйте ще.')
    conn.close()
