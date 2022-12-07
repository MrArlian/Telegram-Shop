from aiogram import types

from database import DataBase, models
from modules import Settings
from keyboard import reply

import texts


db = DataBase(Settings.DatabaseUrl)


async def starting(message: types.Message):
    db.add(models.User, 'id', id=message.chat.id)
    await message.answer(texts.start_message, reply_markup=reply.main_menu)
