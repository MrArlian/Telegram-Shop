from aiogram.dispatcher.filters import Text

from keyboard import callbacks
from main import dispatcher

from . import faq, product
from .. import states


ProductFilter = Text((
    'program', 'telegram',
    'instagram', 'account',
    'data', 'service'
))

dispatcher.register_message_handler(product.category, Text('🔥 категории товаров', ignore_case=True))
dispatcher.register_callback_query_handler(product.category, Text('category'))

dispatcher.register_callback_query_handler(product.view_products, ProductFilter)
dispatcher.register_callback_query_handler(product.view_product, callbacks.ProductInfo.filter())

dispatcher.register_callback_query_handler(product.buy_product, callbacks.BuyProduct.filter())
dispatcher.register_message_handler(product.number_product, state=states.BuyProduct.number)

dispatcher.register_message_handler(faq.faq, Text('💡 правила', ignore_case=True))
dispatcher.register_message_handler(faq.partners, Text('🤝 наши партнеры', ignore_case=True))
