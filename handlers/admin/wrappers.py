from aiogram.dispatcher.storage import FSMContext
from aiogram import types

from keyboard import reply

import texts


def back_admin_menu(func):
    async def wrapper(message: types.Message, state: FSMContext):

        if (message.text or '').lower() == 'отмена':
            await message.answer(texts.back, reply_markup=reply.admin_menu)
            return await state.finish()

        await func(message, state)

    return wrapper
