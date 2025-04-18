from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update
from aiogram.enums import ParseMode
import logging

# Импортируем конфигурацию и роутеры
from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH
from handlers import commands, forward_handler

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем экземпляры бота и диспетчера
default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=BOT_TOKEN, default=default_properties)
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(commands.router)
dp.include_router(forward_handler.router)

# Создаем FastAPI-приложение
app = FastAPI()

# Настройка webhook при запуске сервера
@app.on_event("startup")
async def on_startup():
    logger.info("Запуск приложения...")
    try:
        # Устанавливаем webhook
        await bot.set_webhook(WEBHOOK_URL)
        logger.info(f"Webhook установлен: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Ошибка при установке webhook: {e}")

# Маршрут для обработки обновлений от Telegram
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    logger.info("Получено обновление от Telegram")
    try:
        # Получаем данные из запроса
        update_data = await request.json()
        logger.debug(f"Данные обновления: {update_data}")
        # Преобразуем данные в объект Update
        update = Update.model_validate(update_data)
        # Передаем обновление в диспетчер
        await dp.feed_update(bot, update)
        logger.info("Обновление успешно обработано.")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Ошибка при обработке обновления: {e}")
        return {"status": "error", "message": str(e)}

# Тестовый маршрут для проверки работоспособности сервера
@app.get("/")
async def root():
    return {"status": "ok"}