from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from config import BOT_TOKEN
from handlers import commands, forward_handler

app = FastAPI()
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(commands.router)
dp.include_router(forward_handler.router)

# Настройка Webhook
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook("https://pricehunter-l7rb.onrender.com")

# Обработка входящих обновлений от Telegram
@app.post("/webhook")
async def telegram_webhook(update: dict):
    telegram_update = Update.model_validate(update)
    await dp.feed_update(bot, telegram_update)

# Healthcheck
@app.get("/")
async def root():
    return {"status": "ok"}