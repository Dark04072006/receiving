from PIL import Image
from io import BytesIO
from requests import get
from typing import TypeAlias

ImageBytes: TypeAlias = BytesIO


def get_image_with_logo(product_image_url: str) -> ImageBytes:
    bio = BytesIO()
    # # Загрузите изображения
    response = get(product_image_url)

    header_image = Image.open("media/header.png")
    product_image = Image.open(BytesIO(response.content))

    # Определите размеры изображений
    header_width, header_height = header_image.size
    product_width, product_height = product_image.size

    # Определите размеры и отступы для нового изображения
    padding = 20  # Величина отступов
    output_width = header_width + 2 * padding
    output_height = header_height + product_height + 3 * padding

    # Создайте новое изображение с размерами, соответствующими вашему HTML
    output_image = Image.new("RGBA", (output_width, output_height),
                             (255, 255, 255, 0))

    # Вставьте шапку сайта с отступами сверху и слева
    output_image.paste(header_image, (padding, padding))

    # Вставьте изображение товара с отступами снизу и по центру по горизонтали
    offset_x = (output_width - product_width) // 2
    output_image.paste(product_image, (offset_x, header_height + 2 * padding))

    bio.name = 'output_image.png'
    # Сохраните результат
    output_image.save(bio, 'PNG')

    bio.seek(0)

    return bio
