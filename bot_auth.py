from uuid import uuid4

from aiogram import F
from aiogram.client.session import aiohttp
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config import WEBHOOK_URL
from models import User
from setup import dp


@dp.message(F.text == '/restart')
async def receive_contact(message: Message):
    user = await User.get_or_none(telegram_id=message.from_user.id)
    if not user:
        return await message.answer('You have not registered!')
    else:
        user_token = str(uuid4())
        phone = user.phone
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    WEBHOOK_URL + '/generate-token' + '/' + user_token + '/' + f'{message.from_user.id}:{phone}' + '/' + 'secret_key') as resp:
                result = await resp.json()
                if 'success' in result:
                    await session.close()
                    return await message.answer(f'{WEBHOOK_URL}/enter/{user_token}', disable_web_page_preview=True)


@dp.message(F.text.startswith('/start'))
async def echo_handler(message: Message):
    user = await User.get_or_none(telegram_id=message.from_user.id)
    if user:
        return await message.answer('You have already registered!')
    answer_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='Send phone number', request_contact=True)
        ]
    ], resize_keyboard=True)
    await message.answer('Hi! Give me your phon number',
                         reply_markup=answer_keyboard)


@dp.message(F.contact)
async def receive_contact(message: Message):
    phone = message.contact.phone_number
    user = await User.get_or_none(telegram_id=message.from_user.id)
    if user:
        return await message.answer('You have already registered!')
    else:
        user_token = str(uuid4())
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    WEBHOOK_URL + '/generate-token' + '/' + user_token + '/' + f'{message.from_user.id}:{phone}' + '/' + 'secret_key') as resp:
                result = await resp.json()
                if 'success' in result:
                    await session.close()
                    return await message.answer(f'{WEBHOOK_URL}/enter/{user_token}', disable_web_page_preview=True)
