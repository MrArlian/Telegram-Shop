import typing
import time

from aiogram.dispatcher.storage import FSMContext
from aiogram import types

from keyboard import ProductInfo, BuyProduct, inline
from modules import Settings, FreeKassa, tools
from database import DataBase, models
from main import storage

import texts

from .. import states


kassa = FreeKassa(Settings.ApiKey, Settings.ShopId, Settings.Secret)
db = DataBase(Settings.DatabaseUrl)


async def category(event: typing.Union[types.Message, types.CallbackQuery]):

    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(texts.category_select, reply_markup=inline.category_menu)
    else:
        await event.answer(texts.category_select, reply_markup=inline.category_menu)

async def view_products(callback: types.CallbackQuery):

    products = db.get_all_data(models.Product, category=callback.data)

    markup = types.InlineKeyboardMarkup(2)
    markup.add(types.InlineKeyboardButton('Назад', callback_data='category'))
    markup.inline_keyboard.append([])


    if not products:
        return await callback.answer(texts.no_product)

    for product in products:
        markup.insert(types.InlineKeyboardButton(
            text=product.name, callback_data=ProductInfo.new(product.id)
        ))

    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(texts.choose_product, reply_markup=markup)
    else:
        await callback.message.edit_text(texts.choose_product, reply_markup=markup)

async def view_product(callback: types.CallbackQuery, callback_data: dict):

    product = db.get_data(models.Product, id=callback_data.get('id'))

    number = tools.file_counter(product.category, product.id)

    markup = types.InlineKeyboardMarkup(1)
    item1 = types.InlineKeyboardButton('Купить', callback_data=BuyProduct.new(product.id))
    item2 = types.InlineKeyboardButton('Назад', callback_data=product.category)
    markup.add(*(item1, item2) if number > 0 else (item2,))


    if product.category in ('telegram', 'instagram', 'account'):
        msg = texts.product_info_v1.format(product.name, product.price, number, product.description)
    else:
        msg = texts.product_info_v2.format(product.name, product.price, product.description)

    if product.media_link:
        file = types.InputFile(product.media_link)
        await callback.message.answer_photo(file, msg, reply_markup=markup)
        return await callback.message.delete()

    await callback.message.edit_text(msg, reply_markup=markup)

async def buy_product(callback: types.CallbackQuery, callback_data: dict):

    product_id = callback_data.get('id')
    user_id = callback.from_user.id

    product = db.get_data(models.Product, id=product_id)
    order_id = int(time.time())

    await callback.message.delete_reply_markup()


    if product.category in ('program', 'data', 'service'):
        url = kassa.generate_payment_url(product.price, order_id)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Оплатить FreeKassa', url=url))

        db.add(
            table=models.Transaction,
            id=order_id,
            user_id=user_id,
            product_id=product.id,
            path=product.file_link
        )
        msg = texts.order.format(order_id, product.category, 1, product.price, product.price)
        return await callback.message.answer(msg, reply_markup=markup)

    await storage.update_data(user=user_id, product_id=product_id)
    await callback.message.answer(texts.enter_quantity)
    await states.BuyProduct.number.set()

async def number_product(message: types.Message, state: FSMContext):

    user_id = message.chat.id
    text = message.text

    data = await state.get_data()
    product_id = data.get('product_id')

    product = db.get_data(models.Product, id=product_id)


    if tools.is_digit(text, True):
        number = int(text)

        if number > tools.file_counter(product.category, product_id):
            return await message.answer(texts.not_enough)
        if number < 1:
            return await message.answer(texts.minimum_input)

        total_price = product.price * number
        order_id = int(time.time())

        tmp_dir = tools.move_tmp_dir(product.category, product_id, number, user_id)
        url = kassa.generate_payment_url(total_price, order_id)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Оплатить FreeKassa', url=url))

        db.add(
            table=models.Transaction,
            id=order_id,
            user_id=user_id,
            product_id=product_id,
            path=tmp_dir
        )
        msg = texts.order.format(order_id, product.category, number, product.price, total_price)
        await message.answer(msg, reply_markup=markup)
        await state.finish()

    else:
        await message.answer(texts.input_error)
