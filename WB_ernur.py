from database import (
    init_db, get_all_products, insert_new_product, create_indexes,
    get_products_without_name_and_id, get_products_cheaper_than_10000,
    create_view_cheaper_than_10000
)
from core import (
    process_article, generate_random_articles, search_articles_by_keyword,
    process_many_random_articles
)

def main_menu():
    while True:
        print("\nМеню:")
        print("1) Вывод всех товаров")
        print("2) Вставка нового товара в БД")
        print("3) Создание правильных индексов на БД")
        print("4) Массовый сбор случайных артикулов")
        print("5) Поиск по ключевому слову")
        print("6) Поиск по артикулу")
        print("7) Вывод товаров без описания (имени и id)")
        print("8) Вывод товаров дешевле 10 000")
        print("9) Создать представление товаров дешевле 10 000")
        print("10) Поиск по индексу (ID)")
        print("0) Выйти")
        choice = input("Выберите пункт меню: ").strip()
        
        if choice == "1":
            for row in get_all_products(order_by="id"):
                print(row)
        elif choice == "2":
            insert_new_product()
        elif choice == "3":
            create_indexes()
        elif choice == "4":
            total = int(input("Сколько товаров собрать? "))
            length = int(input("Длина артикула (7, 8, 9): "))
            pause = float(input("Пауза между запросами (сек): "))
            process_many_random_articles(total=total, length=length, pause=pause)
        elif choice == "5":
            keyword = input("Введите ключевое слово: ").strip()
            if keyword:
                articles = search_articles_by_keyword(keyword, count=5)
                for art in articles:
                    process_article(art)
        elif choice == "6":
            user_articles = input("Введите артикулы через запятую: ").strip()
            if user_articles:
                articles_list = [art.strip() for art in user_articles.split(',') if art.strip()]
                for art in articles_list:
                    process_article(art)
        elif choice == "7":
            for row in get_products_without_name_and_id():
                print(row)
        elif choice == "8":
            for row in get_products_cheaper_than_10000():
                print(row)
        elif choice == "9":
            create_view_cheaper_than_10000()
        elif choice == "10":
            idx = input("Введите ID товара: ").strip()
            if idx.isdigit():
                from database import DB_NAME
                import sqlite3
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("SELECT * FROM products WHERE id = ?", (int(idx),))
                row = c.fetchone()
                conn.close()
                if row:
                    print(f"ID: {row[0]}, Название: {row[1]}, Характеристики: {row[2]}, Цена: {row[3]}, Артикул: {row[4]}")
                else:
                    print("Товар с таким ID не найден.")
            else:
                print("Некорректный ID!")
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Некорректный выбор!")

if __name__ == "__main__":
    init_db()
    main_menu()