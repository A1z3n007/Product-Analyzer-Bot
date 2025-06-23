import sqlite3

DB_NAME = 'database/catalog.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            characteristics TEXT,
            price INTEGER,
            article TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def insert_product(name, characteristics, price, article):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO products (name, characteristics, price, article)
        VALUES (?, ?, ?, ?)
    ''', (name, characteristics, price, article))
    conn.commit()
    conn.close()

def get_all_products(order_by="id"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if order_by not in ("id", "price", "name", "article"):
        order_by = "id"
    c.execute(f'SELECT * FROM products ORDER BY {order_by}')
    rows = c.fetchall()
    conn.close()
    result = []
    for row in rows:
        # row: (id, name, characteristics, price, article)
        text = f"ID: {row[0]}, Название: {row[1]}, Характеристики: {row[2]}, Цена: {row[3]}, Артикул: {row[4]}"
        result.append(text)
    return result


def insert_new_product():
    name = input("Название: ")
    characteristics = input("Характеристики: ")
    price = int(input("Цена: "))
    article = input("Артикул: ")
    insert_product(name, characteristics, price, article)
    print("Товар добавлен.")

def create_indexes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('CREATE INDEX IF NOT EXISTS idx_price ON products(price)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_characteristics ON products(characteristics)')
    conn.commit()
    conn.close()
    print("Индексы созданы.")

def get_products_without_name_and_id():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE (name IS NULL OR name="") OR (id IS NULL)')
    rows = c.fetchall()
    conn.close()
    return rows

def get_products_cheaper_than_10000():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE price < 10000')
    rows = c.fetchall()
    conn.close()
    return rows

def create_view_cheaper_than_10000():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE VIEW IF NOT EXISTS view_cheaper_than_10000 AS
        SELECT * FROM products WHERE price < 10000 ORDER BY price ASC
    ''')
    conn.commit()
    conn.close()
    print("Представление создано.")
