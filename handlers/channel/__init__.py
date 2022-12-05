from aiogram import types

from main import dispatcher

from . import channel


ContentType = types.ContentType.NEW_CHAT_MEMBERS

#channel.py
dispatcher.register_message_handler(channel.user_join, content_types=ContentType)
dispatcher.register_chat_join_request_handler(channel.user_join)
