from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from main import dispatcher

from .. import states
from . import product


DOCS = ContentType.DOCUMENT
PHOTO = ContentType.PHOTO


PhotoMenuFilter = Text(
    equals=('Отмена', 'пропустить'),
    ignore_case=True
)

dispatcher.register_message_handler(product.add_product, Text('добавить товар', ignore_case=True))

dispatcher.register_message_handler(product.add_product_category, state=states.AddProduct.category)

dispatcher.register_message_handler(product.add_product_info, state=states.AddProduct.info)

dispatcher.register_message_handler(product.add_product_photo, PhotoMenuFilter, state=states.AddProduct.photo)
dispatcher.register_message_handler(product.add_product_photo, state=states.AddProduct.photo, content_types=PHOTO)

dispatcher.register_message_handler(product.add_product_data, Text('Отмена'), state=states.AddProduct.data)
dispatcher.register_message_handler(product.add_product_data, state=states.AddProduct.data, content_types=DOCS)
