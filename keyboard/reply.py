from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#User
main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton('🔥 Категории товаров')
        ],
        [
            KeyboardButton('💡 Правила'),
            KeyboardButton('🤝 Наши партнеры')
        ]
    ]
)

#Admin
admin_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton('Добавить товар')
        ]
    ]
)

category_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton('Софты и программы')
        ],
        [
            KeyboardButton('Telegram Аккаунты'),
            KeyboardButton('Instagram Аккаунты')
        ],
        [
            KeyboardButton('Аккаунты - подписки'),
            KeyboardButton('Базы')
        ],
        [
            KeyboardButton('Заказать услугу')
        ],
        [
            KeyboardButton('Отмена')
        ]
    ]
)

add_photo = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton('Пропустить')
        ],
        [
            KeyboardButton('Отмена')
        ]
    ]
)

cancel = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton('Отмена')
        ]
    ]
)
