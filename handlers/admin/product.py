import random
import io
import os
import re

from aiogram.dispatcher.storage import FSMContext
from aiogram import types

from database import DataBase, models
from modules import Settings, tools
from static.data import CATEGORY
from keyboard import reply
from main import bot

import texts

from . import wrappers
from .. import states


PRODUCT_PATH = os.path.join(os.path.split(os.path.abspath('.'))[0], 'storage', 'products')

db = DataBase(Settings.DatabaseUrl)


async def add_product(message: types.Message):
    await message.answer(texts.category_select, reply_markup=reply.category_menu)
    await states.AddProduct.category.set()

@wrappers.back_admin_menu
async def add_product_category(message: types.Message, state: FSMContext):

    category = CATEGORY.get(message.text.lower())


    if not category:
        return await message.answer(texts.category_not_found)

    await message.answer(texts.product_information, reply_markup=reply.cancel)
    await state.update_data(category=category)
    await states.AddProduct.next()

@wrappers.back_admin_menu
async def add_product_info(message: types.Message, state: FSMContext):

    args = re.split(r'\s*[,]\s*', message.text)[:3]


    if len(args) < 3:
        return await message.answer(texts.err_args)
    if not tools.is_digit(args[1]):
        return await message.answer(texts.price_entry_error)

    await message.answer(texts.add_photo, reply_markup=reply.add_photo)
    await state.update_data(args=args)
    await states.AddProduct.next()

@wrappers.back_admin_menu
async def add_product_photo(message: types.Message, state: FSMContext):

    photo = message.photo

    data = await state.get_data()
    category = data.get('category')
    args = data.get('args')

    product_id = random.randint(9999, 999999999)
    path = os.path.join(PRODUCT_PATH, category, str(product_id))


    if photo:
        media_link = os.path.join(path, 'picture.jpg')
    else:
        media_link = ''

    if media_link:
        file = await bot.get_file(photo[-1].file_id)
        await bot.download_file(file.file_path, media_link)

    if category == 'service':
        db.add(
            table=models.Product,
            id=product_id,
            name=args[0],
            price=args[1],
            category=category,
            description=args[2],
            media_link=media_link
        )
        await message.answer(texts.product_added.format(args[0]), reply_markup=reply.admin_menu)
        return await state.finish()

    await message.answer(texts.add_zip_file, reply_markup=reply.remove)
    await state.update_data(product_id=product_id, media=media_link)
    await states.AddProduct.next()

async def add_product_data(message: types.Message, state: FSMContext):

    document = message.document

    data = await state.get_data()
    product_id = data.get('product_id')
    category = data.get('category')
    media_link = data.get('media')
    args = data.get('args')

    path = os.path.join(PRODUCT_PATH, category, str(product_id))


    if document.mime_type != 'application/zip':
        return await message.answer(texts.file_not_valid)

    file = await bot.get_file(document.file_id)
    buf = await bot.download_file(file.file_path, io.BytesIO())

    if category in ('telegram', 'instagram', 'account'):
        tools.extract(buf, path)
    elif category in ('program', 'base'):
        tools.save_archive(buf, document.file_name, path)
        path = os.path.join(path, document.file_name)

    db.add(
        table=models.Product,
        id=product_id,
        name=args[0],
        price=args[1],
        category=category,
        description=args[2],
        media_link=media_link,
        file_link=path
    )
    await message.answer(texts.product_added.format(args[0]), reply_markup=reply.admin_menu)
    await state.finish()
