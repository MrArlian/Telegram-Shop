from aiogram import types

from database import DataBase, models
from modules import Settings
from keyboard import reply

import texts


db = DataBase(Settings.DatabaseUrl)


async def starting(message: types.Message):

    username = message.chat.username
    user_id = message.chat.id

    db.add(models.User, conflicts='id', id=user_id, username=username)

    await message.answer(texts.start_message, reply_markup=reply.main_menu)
