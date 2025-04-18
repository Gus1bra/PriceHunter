import asyncio
import sys
from aiogram import Bot, Dispatcher
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

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(commands.router)
dp.include_router(forward_handler.router)

# Настройка webhook (если используется)
async def on_startup(bot: Bot):
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)

# Точка входа
async def main():
    # Выбор режима работы: polling или webhook
    if WEBHOOK_URL:
        print("Запуск бота с использованием Webhook...")
        await dp.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
        )
    else:
        print("Запуск бота с использованием Polling...")
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())