import asyncio
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH
from handlers import commands, forward_handler

# Установка правильного цикла событий для Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass  # Используем стандартный event loop на Linux, если uvloop недоступен

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
    # Выбор режима работы: polling или webhook
    if WEBHOOK_URL:
        print("Запуск бота с использованием Webhook...")
        try:
            from api.main import run_webhook  # Импортируем функцию запуска FastAPI
            await run_webhook(dp, bot)
        except ImportError as e:
            print(f"Ошибка при импорте FastAPI: {e}")
            print("Переключение на Polling...")
            await dp.start_polling(bot)
    else:
        print("Запуск бота с использованием Polling...")
        await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")