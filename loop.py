import datetime
import asyncio
import os

from aiogram import types, exceptions
from sqlalchemy import func
from pytz import timezone

from database import DataBase, models
from modules import Settings, tools
from keyboard import inline
from main import bot

import texts


TZ = timezone('Europe/Simferopol')

db = DataBase(Settings.DatabaseUrl)


async def task_1() -> None:

    while True:
        await asyncio.sleep(600)

        transactions = db.get_all_data(
            table=models.Transaction,
            conditions=[
                func.now() - models.Transaction.date >= '10 minutes',
                models.Transaction.platform == 'telegram',
                models.Transaction.status == 'wait'
            ]
        )

        for transaction in transactions:
            tools.move_main_dir(transaction.tmp_path)
            db.update_by_id(models.Transaction, transaction.id, status='cancel')

            try:
                await bot.send_message(
                    chat_id=transaction.user_id,
                    text=texts.order_expired.format(transaction.id)
                )
            except (exceptions.BotBlocked, exceptions.UserDeactivated, exceptions.ChatNotFound):
                pass

async def task_2() -> None:
    file = types.InputFile(os.path.join(os.path.abspath('.'), 'static', 'picture.jpg'))

    while True:
        now = datetime.datetime.now()
        delta = datetime.timedelta(
            hours=now.hour,
            minutes=now.minute,
            seconds=now.second
        )
        await asyncio.sleep(214200 - delta.total_seconds())

        for user in db.get_all_data(models.User):
            try:
                await bot.send_photo(
                    chat_id=user.id,
                    photo=file,
                    caption=texts.message,
                    reply_markup=inline.abount_menu
                )
            except (exceptions.BotBlocked, exceptions.UserDeactivated, exceptions.ChatNotFound):
                pass
