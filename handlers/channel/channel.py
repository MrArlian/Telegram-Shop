import typing
import os

from aiogram import types

from main import bot
from keyboard import inline

import texts


async def user_join(event: typing.Union[types.Message, types.ChatJoinRequest]):

    if isinstance(event, types.ChatJoinRequest):
        await event.approve()

    file = types.InputFile(os.path.join(os.path.abspath('.'), 'static', 'picture.jpg'))
    await bot.send_photo(event.from_user.id, file, texts.message, reply_markup=inline.abount_menu)
