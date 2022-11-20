from aiogram import types

import texts


async def faq(message: types.Message):
    await message.answer(texts.faq)

async def partners(message: types.Message):
    await message.answer(texts.partners)
