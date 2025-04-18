import asyncio
import sys

# Установка правильного цикла событий для Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties  # Импортируем DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
from config import BOT_TOKEN
from handlers import commands, forward_handler

# Создаем объект DefaultBotProperties с нужным parse_mode
default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)

# Передаем default_properties в конструктор Bot
bot = Bot(token=BOT_TOKEN, default=default_properties)
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(commands.router)
dp.include_router(forward_handler.router)

# Точка входа
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())