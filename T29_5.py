import sqlite3
import os

DB_FILE = 'suppliers_products.db'

def init_db():
    new_db = not os.path.exists(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if new_db:
        c.execute('''
            CREATE TABLE suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                contact TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE supplies (
                supplier_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                PRIMARY KEY (supplier_id, product_id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        conn.commit()
    return conn

def add_supplier(conn):
    name = input('Назва постачальника: ').strip()
    contact = input('Контактні дані: ').strip()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO suppliers(name, contact) VALUES (?, ?)', (name, contact))
        conn.commit()
        print('Постачальника додано.')
    except sqlite3.IntegrityError:
        print('Постачальник з такою назвою вже існує.')

def add_product(conn):
    name = input('Назва товару: ').strip()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO products(name) VALUES (?)', (name,))
        conn.commit()
        print('Товар додано.')
    except sqlite3.IntegrityError:
        print('Товар з такою назвою вже існує.')

def link_supply(conn):
    supplier = input('Назва постачальника: ').strip()
    product = input('Назва товару: ').strip()
    c = conn.cursor()
    c.execute('SELECT id FROM suppliers WHERE name = ?', (supplier,))
    sup = c.fetchone()
    c.execute('SELECT id FROM products WHERE name = ?', (product,))
    prod = c.fetchone()
    if not sup:
        print('Постачальник не знайдений.')
        return
    if not prod:
        print('Товар не знайдений.')
        return
    try:
        c.execute('INSERT INTO supplies(supplier_id, product_id) VALUES (?, ?)', (sup[0], prod[0]))
        conn.commit()
        print(f'Постачальник "{supplier}" тепер постачає "{product}".')
    except sqlite3.IntegrityError:
        print('Цей зв\'язок вже існує.')

def find_suppliers_by_product(conn):
    product = input('Назва товару для пошуку: ').strip()
    c = conn.cursor()
    c.execute('''
        SELECT s.name, s.contact
        FROM suppliers AS s
        JOIN supplies AS sp ON s.id = sp.supplier_id
        JOIN products AS p ON p.id = sp.product_id
        WHERE p.name = ?
    ''', (product,))
    rows = c.fetchall()
    if rows:
        print(f'Постачальники, які постачають "{product}":')
        for name, contact in rows:
            print(f'  - {name} (контакт: {contact})')
    else:
        print('Немає постачальників для цього товару.')

def find_products_by_supplier(conn):
    supplier = input('Назва постачальника для пошуку: ').strip()
    c = conn.cursor()
    c.execute('''
        SELECT p.name
        FROM products AS p
        JOIN supplies AS sp ON p.id = sp.product_id
        JOIN suppliers AS s ON s.id = sp.supplier_id
        WHERE s.name = ?
    ''', (supplier,))
    rows = c.fetchall()
    if rows:
        print(f'Товари, які постачає "{supplier}":')
        for (name,) in rows:
            print(f'  - {name}')
    else:
        print('Цей постачальник не постачає товари або не знайдений.')

if __name__ == '__main__':
    conn = init_db()
    while True:
        print('\nМеню:')
        print('1. Додати постачальника')
        print('2. Додати товар')
        print('3. Зареєструвати постачання (постачальник → товар)')
        print('4. Пошук постачальників за назвою товару')
        print('5. Пошук товарів за назвою постачальника')
        print('6. Вихід')
        choice = input('Ваш вибір: ').strip()
        if choice == '1':
            add_supplier(conn)
        elif choice == '2':
            add_product(conn)
        elif choice == '3':
            link_supply(conn)
        elif choice == '4':
            find_suppliers_by_product(conn)
        elif choice == '5':
            find_products_by_supplier(conn)
        elif choice == '6':
            print('Вихід...')
            break
        else:
            print('Невірний вибір.')
    conn.close()
