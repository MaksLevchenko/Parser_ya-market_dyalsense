import json
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from parser_ya import get_funk
from aiogram.utils.markdown import hlink, hbold
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('bot_token'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Геймпады']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    await message.answer('Товары со скидкой!', reply_markup=keyboard)


@dp.message_handler(Text(equals='Геймпады'))
async def get_discount(message: types.Message):
    await message.answer('Пожалуйста подождите...')
    get_funk()

    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        for item in data:
            card = f"{hlink(item.get('name_gamepad'), item.get('link'))}\n" \
                   f"{hbold('Цена: ')} {item.get('price')}"
            await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
