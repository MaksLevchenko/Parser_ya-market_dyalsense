import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from parser_ya import get_funk
from aiogram.utils.markdown import hlink, hbold


bot = Bot(token='5629539803:AAHSbyw2rVg9L2Noq4wBIElEZ3Ua7f-TvI8', parse_mode=types.ParseMode.HTML)
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
