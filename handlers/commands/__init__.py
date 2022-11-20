from aiogram.dispatcher.filters import CommandStart, Command

from main import dispatcher
from . import start, admin


dispatcher.register_message_handler(admin.admin_panel, Command('admin'))

dispatcher.register_message_handler(start.starting, CommandStart())
