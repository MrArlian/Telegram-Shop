from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
