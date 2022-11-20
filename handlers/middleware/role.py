from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import types

from modules import Settings


class CheckAdminRole(BaseMiddleware):
    """
        Checks the user role.
    """

    async def on_process_message(self, message: types.Message, *_) -> None:
        if (message.text or '').lower() in ('/admin', 'добавить товар') and \
            message.chat.id != Settings.Admin:
            raise CancelHandler
