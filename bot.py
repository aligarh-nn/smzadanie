import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config['TELEGRAM']['BOT_TOKEN']
bot = Bot(token="8049424222:AAFhKM19Q9eCxDd9hq2LPBxKAAOA1QnNvC4", parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Это бот для почасового производственного анализа.\n\n"
        "Команды:\n"
        "/смена — начать сменный отчёт\n"
        "/час — внести почасовой результат\n"
        "/простой — зафиксировать простой\n"
        "/итог — завершить смену"
    )

@dp.message(Command("смена"))
async def смена(message: Message):
    await message.answer("Смена начата. Введите: Тип работ, бригада, смена.")

@dp.message(Command("час"))
async def час(message: Message):
    await message.answer("Введите время, объём (м), отклонения.")

@dp.message(Command("простой"))
async def простой(message: Message):
    await message.answer("Введите время и причину простоя.")

@dp.message(Command("итог"))
async def итог(message: Message):
    await message.answer("Смена завершена. Данные отправлены в таблицу.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(dp)  # если используешь роутеры
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

