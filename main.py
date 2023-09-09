import logging
import threading
from use_cases.products import send_new_products, send_old_products

logging.basicConfig(level=logging.INFO)


def main() -> None:
    # Create threads for both functions
    new_product_thread = threading.Thread(target=send_new_products)
    old_products_thread = threading.Thread(target=send_old_products)

    # Start the threads
    new_product_thread.start()
    old_products_thread.start()

    # Wait for both threads to finish (you can remove this if not needed)
    new_product_thread.join()
    old_products_thread.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Бот завершил работу")
