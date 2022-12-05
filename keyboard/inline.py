from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


abount_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Отзывы', url='https://t.me/+canmsEFxSa04MmE6')
        ],
        [
            InlineKeyboardButton('Кейсы и портфолио', url='https://t.me/+LE9KjNf35OFlMDYy')
        ],
        [
            InlineKeyboardButton('Наши услуги', url='https://t.me/c/1681438125/3')
        ],
        [
            InlineKeyboardButton('Связь со мной', url='https://t.me/marketingdream')
        ]
    ]
)

category_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Софты и программы', callback_data='program')
        ],
        [
            InlineKeyboardButton('Telegram Аккаунты', callback_data='telegram'),
            InlineKeyboardButton('Instagram Аккаунты', callback_data='instagram')
        ],
        [
            InlineKeyboardButton('Аккаунты - подписки', callback_data='account'),
            InlineKeyboardButton('Базы', callback_data='data')
        ],
        [
            InlineKeyboardButton('Заказать услугу', callback_data='service')
        ]
    ]
)
