import sqlite3
import os
import datetime

DB_FILE = 'garden.db'

def init_db():
    new_db = not os.path.exists(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if new_db:
        c.execute('''
            CREATE TABLE species (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE varieties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                species_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                UNIQUE(species_id, name),
                FOREIGN KEY (species_id) REFERENCES species(id)
            )
        ''')
        c.execute('''
            CREATE TABLE trees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                variety_id INTEGER NOT NULL,
                year_planted INTEGER NOT NULL,
                location TEXT,
                FOREIGN KEY (variety_id) REFERENCES varieties(id)
            )
        ''')
        c.execute('''
            CREATE TABLE harvests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tree_id INTEGER NOT NULL,
                year INTEGER NOT NULL,
                quantity REAL NOT NULL,
                FOREIGN KEY (tree_id) REFERENCES trees(id),
                UNIQUE(tree_id, year)
            )
        ''')
        conn.commit()
    return conn

def add_species(conn):
    name = input('Назва роду дерев: ').strip()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO species(name) VALUES (?)', (name,))
        conn.commit()
        print('Рід додано.')
    except sqlite3.IntegrityError:
        print('Такий рід вже існує.')


def add_variety(conn):
    species = input('Назва роду для сорту: ').strip()
    c = conn.cursor()
    c.execute('SELECT id FROM species WHERE name = ?', (species,))
    row = c.fetchone()
    if not row:
        print('Рід не знайдено.')
        return
    species_id = row[0]
    name = input('Назва сорту: ').strip()
    try:
        c.execute('INSERT INTO varieties(species_id, name) VALUES (?, ?)', (species_id, name))
        conn.commit()
        print('Сорт додано.')
    except sqlite3.IntegrityError:
        print('Такий сорт для цього роду вже існує.')

def add_tree(conn):
    species = input('Рід дерева: ').strip()
    c = conn.cursor()
    c.execute('SELECT id FROM species WHERE name = ?', (species,))
    row = c.fetchone()
    if not row:
        print('Рід не знайдено.')
        return
    species_id = row[0]
    c.execute('SELECT name FROM varieties WHERE species_id = ?', (species_id,))
    varieties = [r[0] for r in c.fetchall()]
    if not varieties:
        print('У цьому роді відсутні сорти.')
        return
    print('Доступні сорти:')
    for v in varieties:
        print(' -', v)
    variety = input('Виберіть сорт: ').strip()
    c.execute('SELECT id FROM varieties WHERE species_id = ? AND name = ?', (species_id, variety))
    row = c.fetchone()
    if not row:
        print('Сорт не знайдено.')
        return
    variety_id = row[0]
    year = input('Рік посадки (YYYY): ').strip()
    try:
        year = int(year)
    except ValueError:
        print('Некоректний рік.')
        return
    location = input('Місце посадки: ').strip()
    c.execute('INSERT INTO trees(variety_id, year_planted, location) VALUES (?, ?, ?)',
              (variety_id, year, location))
    conn.commit()
    print('Дерево додано.')

def add_harvest(conn):
    tree_id = input('ID дерева: ').strip()
    try:
        tree_id = int(tree_id)
    except ValueError:
        print('Некоректний ID.')
        return
    year = input('Рік врожаю (YYYY): ').strip()
    qty = input('Кількість врожаю (кг): ').strip()
    try:
        year = int(year)
        qty = float(qty)
    except ValueError:
        print('Некоректні дані.')
        return
    c = conn.cursor()
    try:
        c.execute('INSERT INTO harvests(tree_id, year, quantity) VALUES (?, ?, ?)',
                  (tree_id, year, qty))
        conn.commit()
        print('Врожай зафіксовано.')
    except sqlite3.IntegrityError:
        print('Врожай для цього року вже існує.')

def show_trees_by_species(conn):
    species = input('Назва роду: ').strip()
    c = conn.cursor()
    c.execute('''
        SELECT t.id, v.name, t.year_planted, t.location
        FROM trees t
        JOIN varieties v ON t.variety_id = v.id
        JOIN species s ON v.species_id = s.id
        WHERE s.name = ?
    ''', (species,))
    rows = c.fetchall()
    if not rows:
        print('Дерева цього роду не знайдено.')
    else:
        print(f'Дерева роду {species}:')
        for tree_id, variety, year, loc in rows:
            print(f'  ID={tree_id}, сорт={variety}, рік={year}, місце="{loc}"')


def show_harvest_for_tree(conn):
    tree_id = input('ID дерева: ').strip()
    try:
        tree_id = int(tree_id)
    except ValueError:
        print('Некоректний ID.')
        return
    start = input('Початковий рік (YYYY): ').strip()
    end = input('Кінцевий рік (YYYY): ').strip()
    try:
        start = int(start)
        end = int(end)
    except ValueError:
        print('Некоректні роки.')
        return
    c = conn.cursor()
    c.execute('''
        SELECT year, quantity
        FROM harvests
        WHERE tree_id = ? AND year BETWEEN ? AND ?
        ORDER BY year
    ''', (tree_id, start, end))
    rows = c.fetchall()
    if not rows:
        print('Даних про врожай не знайдено.')
    else:
        print(f'Врожай дерева {tree_id} за {start}-{end} роки:')
        for year, qty in rows:
            print(f'  {year}: {qty} кг')



if __name__ == '__main__':
    conn = init_db()
    while True:
        print('\nМеню:')
        print('1. Додати рід дерев')
        print('2. Додати сорт')
        print('3. Додати дерево')
        print('4. Додати врожай')
        print('5. Показати дерева за родом')
        print('6. Показати врожай за період')
        print('7. Вихід')
        choice = input('Ваш вибір: ').strip()
        if choice == '1': add_species(conn)
        elif choice == '2': add_variety(conn)
        elif choice == '3': add_tree(conn)
        elif choice == '4': add_harvest(conn)
        elif choice == '5': show_trees_by_species(conn)
        elif choice == '6': show_harvest_for_tree(conn)
        elif choice == '7': break
        else: print('Невірний вибір.')
    conn.close()
