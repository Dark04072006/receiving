import vk_api
from os import getenv
from dotenv import load_dotenv

from use_cases.utils import get_image_with_logo


load_dotenv('files/.env')

token = getenv("VK_TOKEN")
session = vk_api.VkApi(token=token)
vk = session.get_api()
upload = vk_api.VkUpload(session)

group_id = int(getenv('PUBLIC_ID'))
from_group = 0


def send_product_to_public_vk(
    title: str,
    price: str,
    applicability: str,
    image: str,
    url: str
) -> None:
    path = get_image_with_logo(image)

    text = "\nЗдравствуйте, уважаемые покупатели! " + \
           "У нас новое поступление товара, " + \
           "мы всегда рады видеть вас " + \
           "в нашем интернет магазине автозапчастей!\n\n" + \
           f"\nНазвание: {title}" + \
           f"\nПрименимость: {applicability}" + \
           f"\nЦена: {price}",
    image_wall = upload.photo_wall([path])
    attachment = url + ',' + ','.join(
            'photo{owner_id}_{id}'.format(**item) for item in image_wall)

    session.method('wall.post', {
        'access_token': token,
        'from_group': from_group,
        'owner_id': group_id,
        'attachment': attachment,
        'message': text
    })
