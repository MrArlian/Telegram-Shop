from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import types

from database import DataBase, models
from modules import Settings


db = DataBase(Settings.DatabaseUrl)


class CheckAdminRole(BaseMiddleware):
    """
        Checks the user role.
        If using "owner" or "superuser" allows it to the admin panel.
    """

    async def on_process_message(self, message: types.Message, *_) -> None:
        if (message.text or message.caption or '').lower() in ('/admin', 'добавить товар'):
            await self._check(message.chat.id)

    async def _check(self, user_id: int) -> None:
        user = db.get_data(models.User, id=user_id)

        if user.role not in ('owner', 'super_user'):
            raise CancelHandler
