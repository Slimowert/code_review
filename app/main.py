import sys
import time
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

from cookie import get_cookies, headers
import database


def imformation_about_category(url, cookies):
    response = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.find("div", class_="products-page").find('h1', class_="title").text
    category = dict()
    category["name"] = name
    category['url'] = url
    return category


def get_all_urls_of_category(url, cookies):
    # print("Формируется лист ссылок категории")
    urls = []
    next_page = url
    while len(next_page) > 0:
        response = requests.get(next_page, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        urls.extend(get_urls_from_page(soup))
        try:
            next_page = soup.find('button', class_='pagination-widget__show-more-btn')
            next_page = 'https://www.dns-shop.ru' + next_page.get('data-url')
        except AttributeError:
            return urls
    
    return urls


def get_urls_from_page(soup):
    elements = soup.find_all('a', class_="catalog-product__name ui-link ui-link_black") 
    return list(map(lambda element: 'https://www.dns-shop.ru' + element.get("href") + 'characteristics/', elements))


def get_notebook_data(url, cookies):
    notebook = dict()
    
    response = requests.get(
        url,
        cookies=cookies,
        headers=headers,
    )
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    characteristic = soup.find("div", class_="product-characteristics-content")
    groups = characteristic.find_all('div', class_='product-characteristics__group')
    for group in groups:
        specs = group.find_all('div', class_='product-characteristics__spec')
        for spec in specs:
            titles = spec.find('div', class_='product-characteristics__spec-title').text
            value = spec.find('div', class_='product-characteristics__spec-value').text
            notebook[titles.strip()] = value.strip()


    if old_price_element := soup.find('span', class_='product-buy__prev'):
        notebook["price"], notebook["price_without_discount"] = map(int, soup.find('div',class_='product-buy__price product-buy__price_active').text.replace(' ', '').split('₽'))
        notebook["price_without_discount"] = int(old_price_element.text.replace(' ', ''))
        notebook["discount"] = round(100 - (notebook["price"] / notebook["price_without_discount"]) * 100)
    elif price := soup.find('div', class_='product-buy__price'):
        notebook["price"] = int(price.text.replace(' ', '')[:-1])
        notebook["price_without_discount"], notebook["discount"] = 0, 0
    
    notebook["url"] = url

    return notebook


def parser(url):
    start_time = time.time()

    cookies=get_cookies()

    category = imformation_about_category(url, cookies)
    urls = get_all_urls_of_category(url, cookies)

    max_len_dict = dict()
    name_table = category["name"].replace(' ', '_')
    database.delete_table(name_table)
    database.create_table(name_table)
    for url in tqdm(urls, ncols=70, unit='item', colour='green', file=sys.stdout):
        item = get_notebook_data(url , cookies)
        if len(item) > len(max_len_dict):
            max_len_dict = item
        database.add_instance(name_table, item)

    category['characteristics'] = ', '.join(map(str, max_len_dict.keys()))
    database.add_category(category)

    total_time = time.time() - start_time
    print(f"Время выполнения:\n"
          f"{(total_time // 3600):02.0f}:"
          f"{(total_time % 3600 // 60):02.0f}:"
          f"{(total_time % 60):02.0f}")


if __name__ == '__main__':
    parser(sys.argv[1])
    # parser('https://www.dns-shop.ru/catalog/17a9dcd816404e77/instrumenty-dlya-vitoj-pary/')
    # parser('https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/')
    # parser('https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/')
    # parser('https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/')
    # parser('https://www.dns-shop.ru/catalog/17a8ae4916404e77/televizory/')
    # parser('https://www.dns-shop.ru/catalog/8af402e76a6db2e5/elektrosamokaty/')
    # parser('https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/')  очень долго
