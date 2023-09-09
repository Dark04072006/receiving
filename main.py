import logging
import multiprocessing
from use_cases.products import send_new_products, send_old_products

logging.basicConfig(level=logging.INFO)


def main() -> None:
    new_product_process = multiprocessing.Process(target=send_new_products)
    old_product_process = multiprocessing.Process(target=send_old_products)

    new_product_process.start()
    old_product_process.start()

    new_product_process.join()
    old_product_process.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Бот завершил работу")
