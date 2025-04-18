from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.enums import ParseMode

from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH
from handlers import commands, forward_handler

# Создаем экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(commands.router)
dp.include_router(forward_handler.router)

# Создаем FastAPI-приложение
app = FastAPI()

# Настройка webhook при запуске сервера
@app.on_event("startup")
async def on_startup():
    # Устанавливаем webhook
    await bot.set_webhook(WEBHOOK_URL)

# Маршрут для обработки обновлений от Telegram
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    # Получаем данные из запроса
    update_data = await request.json()
    # Преобразуем данные в объект Update
    update = Update.model_validate(update_data)
    # Передаем обновление в диспетчер
    await dp.feed_update(bot, update)
    return {"status": "ok"}

# Тестовый маршрут для проверки работоспособности сервера
@app.get("/")
async def root():
    return {"status": "ok"}