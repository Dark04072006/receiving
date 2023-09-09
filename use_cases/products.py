import time
from bs4 import BeautifulSoup
import requests
import vk_api
from typing import Dict, Optional
from bot.telegram import send_product_to_channel
from bot.vk import send_product_to_public_vk
from use_cases.db import Database


db_ = Database()

BASE_URL = 'https://autorevers-parts.ru/'
BASE_CONTENT_PRODUCTS_URL = 'https://autorevers-parts.ru/' \
    'content/files/images/products_images/'


class InfoOfGoods:
    @staticmethod
    def get_catalogue_products(offset: int, limit: int) -> list[dict]:
        query = "SELECT * FROM shop_catalogue_products LIMIT %s OFFSET %s"
        results = db_.execute_query(query % (limit, offset))
        return results

    @staticmethod
    def get_category(id_: int) -> dict:
        query = "SELECT * FROM shop_catalogue_categories WHERE id=%s" % id_
        results = db_.execute_query(query)
        return results

    @staticmethod
    def get_product(id_: int) -> dict:
        query = '''SELECT * FROM shop_catalogue_products WHERE id=%s'''
        return db_.execute_query(query % id_)

    @staticmethod
    def get_applicability(product_id: int) -> dict:
        query = '''
        SELECT * FROM `shop_properties_values_text` WHERE product_id=%s
        '''
        return db_.execute_query(query % product_id)[-1].get('value')

    @staticmethod
    def get_image(product_id: int) -> dict:
        query = '''SELECT * FROM `shop_products_images` WHERE product_id=%s'''
        return db_.execute_query(query % product_id)

    @staticmethod
    def get_total_number_of_products() -> int:
        query = "SELECT COUNT(*) FROM shop_catalogue_products"
        result = db_.execute_query(query)
        return result[0].get('COUNT(*)') if result else 0

    @staticmethod
    def get_price_of_product(product_url: str) -> str:
        text = requests.get(product_url).text
        soup = BeautifulSoup(text, 'lxml')
        div = soup.find('div', {'class': 'price_div_text'})
        return div.get_text().strip()

    @classmethod
    def get_product_info(cls, product: Dict[str, any]) -> Dict[str, any]:
        product_id = product.get('id')
        category_id = product.get('category_id')
        title = product.get('caption')
        alias = product.get('alias')
        category_url = cls.get_category(category_id)[0].get('url')
        image = cls.get_image(product_id)[0].get('file_name')
        applicability = cls.get_applicability(product_id)
        price = cls.get_price_of_product(f"{BASE_URL}{category_url}/{alias}")

        return {
            'title': title,
            'url': f"{BASE_URL}{category_url}/{alias}",
            'image': f"{BASE_CONTENT_PRODUCTS_URL}{image}",
            'applicability': applicability,
            'price': price
        }


def send_new_products() -> None:
    last_id: Optional[int] = None
    while True:
        new_product = InfoOfGoods().get_catalogue_products(
            offset=0, limit=1
        )[0]
        new_id = new_product.get('id')
        if last_id is None:
            last_id = new_id
        elif last_id != new_id:
            print("Отправка новой записи")
            last_id = new_id
            product = InfoOfGoods().get_product(last_id)
            try:
                product = InfoOfGoods().get_product_info(product[0])
            except TypeError:
                continue
            try:
                send_product_to_channel(**product)
            except vk_api.exceptions.ApiError:
                pass
            send_product_to_channel(**product)
            time.sleep(60)


def send_old_products() -> None:
    info = InfoOfGoods()
    limit = 20
    offset = info.get_total_number_of_products() - limit

    while offset >= 0:
        # Получаем следующие 20 товаров, начиная с конца списка
        catalogue_products = info.get_catalogue_products(offset, limit)

        # Отправляем или обрабатываем товары здесь
        for product in catalogue_products:
            try:
                info_ = info.get_product_info(product)
            except TypeError:
                continue
            try:
                send_product_to_public_vk(**info_)
            except vk_api.exceptions.ApiError:
                pass
            send_product_to_channel(**info_)
            time.sleep(60 * 30)

        offset -= limit  # Move to the next batch of products

        if offset < 0:
            break  # Exit the loop when there are no more products to process
