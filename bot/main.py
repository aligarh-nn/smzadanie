import logging
from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
gc = gspread.authorize(credentials)
sheet = gc.open(os.getenv("GOOGLE_SHEET_NAME"))

shift_data = {}
hourly_data = []

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Привет! Давайте начнем сменное задание. Введите название объекта:")

@dp.message_handler(lambda message: 'Название объекта:' not in shift_data)
async def get_object(message: types.Message):
    shift_data['Название объекта'] = message.text
    await message.answer("Тип работы (копка / прокладка):")

@dp.message_handler(lambda message: 'Тип работы' not in shift_data)
async def get_work_type(message: types.Message):
    shift_data['Тип работы'] = message.text
    await message.answer("Номер смены:")

@dp.message_handler(lambda message: 'Номер смены' not in shift_data)
async def get_shift_num(message: types.Message):
    shift_data['Номер смены'] = message.text
    shift_data['Дата'] = datetime.now().strftime('%Y-%m-%d')
    await message.answer("Время начала работы (например, 08:00):")

@dp.message_handler(lambda message: 'Время начала работы' not in shift_data)
async def get_start_time(message: types.Message):
    shift_data['Время начала работы'] = message.text
    await message.answer("Состав бригады:")

@dp.message_handler(lambda message: 'Состав бригады' not in shift_data)
async def get_team(message: types.Message):
    shift_data['Состав бригады'] = message.text
    await message.answer("Плановый объем работ (м):")

@dp.message_handler(lambda message: 'Плановый объем работ (м)' not in shift_data)
async def get_plan(message: types.Message):
    shift_data['Плановый объем работ (м)'] = message.text

    # Запись в таблицу сменного задания
    sheet1 = sheet.worksheet("Сменные задания")
    sheet1.append_row([shift_data.get(k, "") for k in ["Дата", "Номер смены", "Название объекта", "Тип работы", "Время начала работы", "Состав бригады", "Плановый объем работ (м)"]])

    await message.answer("Сменное задание записано ✅. Теперь вводите почасовой анализ. Введите время (например, 08:00–09:00):")

@dp.message_handler()
async def get_hourly(message: types.Message):
    if 'Время' not in shift_data:
        shift_data['Время'] = message.text
        await message.answer("Фактически выполнено (м):")
    elif 'Объем факт' not in shift_data:
        shift_data['Объем факт'] = message.text
        await message.answer("Были ли простои? (да / нет):")
    elif 'Простой' not in shift_data:
        shift_data['Простой'] = message.text
        if message.text.lower() == "да":
            await message.answer("Причина простоя:")
        else:
            shift_data['Причина'] = ""
            await message.answer("Были ли отклонения? Если нет — напишите 'нет':")
    elif 'Причина' not in shift_data:
        shift_data['Причина'] = message.text
        await message.answer("Были ли отклонения? Если нет — напишите 'нет':")
    elif 'Отклонения' not in shift_data:
        shift_data['Отклонения'] = message.text

        # Запись в таблицу почасового анализа
        sheet2 = sheet.worksheet("Почасовой анализ")
        sheet2.append_row([
            shift_data.get("Дата"),
            shift_data.get("Номер смены"),
            shift_data.get("Время"),
            shift_data.get("Объем факт"),
            shift_data.get("Простой"),
            shift_data.get("Причина"),
            shift_data.get("Отклонения")
        ])

        # Очистка почасовых данных
        for key in ["Время", "Объем факт", "Простой", "Причина", "Отклонения"]:
            shift_data.pop(key, None)

        await message.answer("Почасовой отчёт записан ✅. Введите следующее время или команду /start для новой смены.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
