from fastapi import FastAPI, Request
from aiogram import Bot
from aiogram.types import Update
from aiogram.dispatcher.dispatcher import Dispatcher

from config import WEBHOOK_PATH, WEBHOOK_URL

app = FastAPI()
bot = None  # Глобальная переменная для бота
dp = None  # Глобальная переменная для диспетчера

# Функция для запуска FastAPI с webhook
async def run_webhook(dispatcher: Dispatcher, bot_instance: Bot):
    global dp, bot
    dp = dispatcher
    bot = bot_instance
    await bot.set_webhook(WEBHOOK_URL)

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    # Получаем обновление от Telegram
    update_data = await request.json()
    update = Update.model_validate(update_data)
    # Передаем обновление в диспетчер
    await dp.feed_update(bot, update)

@app.get("/")
async def root():
    return {"status": "ok"}