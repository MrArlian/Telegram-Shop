from aiogram import types

from keyboard import reply

import texts


async def admin_panel(message: types.Message):
    await message.answer(texts.hello_admin, reply_markup=reply.admin_menu)
