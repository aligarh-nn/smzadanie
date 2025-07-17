import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import ya_api
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config['TELEGRAM']['BOT_TOKEN']
bot = Bot(token="8049424222:AAFhKM19Q9eCxDd9hq2LPBxKAAOA1QnNvC4")
dp = Dispatcher(bot)

@dp.message_handler()
async def start(message: types.Message):
    await message.answer("Привет! Это бот для почасового производственного анализа.

Команды:
/смена — начать сменный отчёт
/час — внести почасовой результат
/простой — зафиксировать простой
/итог — завершить смену")

@dp.message(Command('смена'))
async def смена(message: types.Message):
    await message.answer("Смена начата. Введите:
Тип работ (копка/прокладка), бригада, смена")

@dp.message(Command('час'))
async def час(message: types.Message):
    await message.answer("Введите данные:
Время, Объём (м), Отклонения")

@dp.message(Command('простой'))
async def простой(message: types.Message):
    await message.answer("Введите время и причину простоя")

@dp.message(Command('итог'))
async def итог(message: types.Message):
    await message.answer("Смена завершена. Данные отправлены в таблицу.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
