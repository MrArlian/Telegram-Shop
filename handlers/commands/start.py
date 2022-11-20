from aiogram import types

from keyboard import reply

import texts


async def starting(message: types.Message):
    await message.answer(texts.start_message, reply_markup=reply.main_menu)
