import asyncio

from sqlalchemy import func

from database import DataBase, models
from modules import Settings, tools
from main import bot

import texts


db = DataBase(Settings.DatabaseUrl)


async def task() -> None:

    while True:
        await asyncio.sleep(600)

        transactions = db.get_all_data(
            table=models.Transaction,
            conditions=[
                func.now() - models.Transaction.deta >= '10 minutes',
                models.Transaction.platform == 'telegram',
                models.Transaction.status == 'wait'
            ]
        )

        for transaction in transactions:
            tools.move_main_dir(transaction.tmp_path)
            db.update_by_id(models.Transaction, transaction.id, status='cancel')

            await bot.send_message(
                chat_id=transaction.user_id,
                text=texts.order_expired.format(transaction.id)
            )
