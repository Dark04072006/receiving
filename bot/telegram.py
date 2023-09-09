from os import getenv
from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from use_cases.utils import get_image_with_logo


load_dotenv('files/.env')


def send_product_to_channel(
        title: str,
        price: str,
        applicability: str,
        image: str,
        url: str
) -> None:
    bot = TeleBot(token=getenv('TG_TOKEN'))
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Подробнее', url=url))
    photo = get_image_with_logo(image)

    bot.send_photo(
        getenv('CHANNEL_NAME'),
        photo=photo,
        caption="\nЗдравствуйте, уважаемые покупатели! " +
                "У нас новое поступление товара, " +
                "мы всегда рады видеть вас " +
                "в нашем интернет магазине автозапчастей!\n\n"
                f"\nНазвание: {title}"
                f"\nПрименимость: {applicability}"
                f"\nЦена: {price}",
        reply_markup=markup
    )
