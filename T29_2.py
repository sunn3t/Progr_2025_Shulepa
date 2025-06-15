import sqlite3
import os

DB_FILE = 'systems.db'

def init_db():
    need_create = not os.path.exists(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    if need_create:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE systems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                address TEXT,
                login TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
    return conn

def add_system(conn):
    name = input('Windows').strip()
    address = input().strip()
    login = input('Логін: ').strip()
    password = input('Пароль: ').strip()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO systems (name, address, login, password) VALUES (?, ?, ?, ?)',
            (name, address if address else None, login, password)
        )
        conn.commit()
        print('Систему додано успішно.')
    except sqlite3.IntegrityError:
        print('Система з такою назвою вже існує.')

def get_credentials(conn):
    name = input('Введіть назву системи для пошуку: ').strip()
    c = conn.cursor()
    c.execute('SELECT address, login, password FROM systems WHERE name = ?', (name,))
    row = c.fetchone()
    if row:
        address, login, password = row
        print(f"Система: {name}")
        print(f"Адреса: {address if address else '(не вказано)'}")
        print(f"Логін: {login}")
        print(f"Пароль: {password}")
    else:
        print('Систему з такою назвою не знайдено.')

if __name__ == '__main__':
    conn = init_db()
    print('=== Менеджер логінів і паролів ===')
    while True:
        print('\nМеню:')
        print('1. Додати систему')
        print('2. Отримати дані за назвою')
        print('3. Вихід')
        choice = input('Ваш вибір: ').strip()
        if choice == '1':
            add_system(conn)
        elif choice == '2':
            get_credentials(conn)
        elif choice == '3':
            print('Вихід...')
            break
        else:
            print('Невірний вибір, спробуйте ще раз.')
    conn.close()
