import requests
import random
import time
from database import insert_product

proxy = {
    "http": "http://5435d268bba805db9446__cr.kz:1ce35e8a9661e50b@gw.dataimpulse.com:10000",
    "https": "http://5435d268bba805db9446__cr.kz:1ce35e8a9661e50b@gw.dataimpulse.com:10022"
}

def get_card_json(article):
    if len(article) == 9:
        url = f"https://alm-basket-cdn-02.geobasket.ru/vol{article[0:4]}/part{article[0:6]}/{article}/info/ru/card.json"
    elif len(article) == 8:
        url = f"https://alm-basket-cdn-03.geobasket.ru/vol{article[0:3]}/part{article[0:5]}/{article}/info/ru/card.json"
    elif len(article) == 7:
        url = f"https://alm-basket-cdn-02.geobasket.ru/vol{article[0:2]}/part{article[0:4]}/{article}/info/ru/card.json"
    else:
        return None
    try:
        resp = requests.get(url, timeout=3, proxies=proxy)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None

def get_price(article):
    if len(article) == 9:
        url = f"https://alm-basket-cdn-03.geobasket.ru/vol{article[0:4]}/part{article[0:6]}/{article}/info/price-history.json"
    elif len(article) == 8:
        url = f"https://alm-basket-cdn-01.geobasket.ru/vol{article[0:3]}/part{article[0:5]}/{article}/info/price-history.json"
    elif len(article) == 7:
        url = f"https://alm-basket-cdn-02.geobasket.ru/vol{article[0:2]}/part{article[0:4]}/{article}/info/price-history.json"
    else:
        return None
    try:
        resp = requests.get(url, timeout=3, proxies=proxy)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and data:
                last_price = data[-1].get("price", None)
                if last_price:
                    return last_price // 100
            return None
    except Exception:
        pass
    return None

def process_article(article):
    rand = random.randint(1000, 10000)
    card = get_card_json(article)
    if not card:
        print(f"Не найдено: {article}")
        return
    name = card.get('imt_name', 'Нет имени')
    characteristics = str(card.get('options', 'Нет характеристик'))
    price = get_price(article)
    insert_product(name, characteristics, rand, article)
    print(f"Сохранено: {name} | {rand} | {article}")

def generate_random_articles(count=10, length=8):
    articles = set()
    while len(articles) < count:
        art = ''.join([str(random.randint(0, 9)) for _ in range(length)])
        articles.add(art)
    return list(articles)

def search_articles_by_keyword(keyword, count=10):
    url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?query={keyword}&resultset=catalog"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            articles = []
            for item in data.get('data', {}).get('products', []):
                art = str(item.get('id'))
                if len(art) in (7, 8, 9):
                    articles.append(art)
                if len(articles) >= count:
                    break
            return articles
    except Exception:
        pass
    return []

def process_many_random_articles(total=1000, length=8, pause=0.5):
    count = 0
    while count < total:
        art = ''.join([str(random.randint(0, 9)) for _ in range(length)])
        try:
            process_article(art)
            count += 1
        except Exception as e:
            print(f"Ошибка при обработке артикула {art}: {e}")
        time.sleep(pause)