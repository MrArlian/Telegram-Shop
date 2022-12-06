import typing
import os

from aiogram import types, exceptions

from database import DataBase, models
from modules import Settings
from keyboard import inline
from main import bot

import texts


db = DataBase(Settings.DatabaseUrl)


async def user_join(event: typing.Union[types.Message, types.ChatJoinRequest]):

    if isinstance(event, types.ChatJoinRequest):
        await event.approve()

    file = types.InputFile(os.path.join(os.path.abspath('.'), 'static', 'picture.jpg'))
    try:
        await bot.send_photo(
            chat_id=event.from_user.id,
            photo=file,
            caption=texts.message,
            reply_markup=inline.abount_menu
        )
    except (exceptions.CantTalkWithBots, exceptions.CantInitiateConversation):
        return

    db.add(models.User, 'id', id=event.from_user.id)
