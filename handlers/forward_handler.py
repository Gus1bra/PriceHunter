from aiogram import Router, F
from aiogram.types import Message
from services.parser import extract_product
from database.models import insert_product
import logging
router = Router()

@router.message(F.forward_from_chat)
async def handle_forward(message: Message):
    result = extract_product(message.text)
    if result:
        name, price = result
        await insert_product(name, price, message.forward_from_chat.title)
        logging.info(f"Parsed product: name={name}, price={price}")
        await message.reply(f"✅ Найдено: {name} — {price} ₽")
    else:
        await message.reply("❌ Не удалось извлечь цену.")

@router.message(F.text)  # Обработка обычных текстовых сообщений
async def handle_text(message: Message):
    result = extract_product(message.text)
    if result:
        name, price = result
        await insert_product(name, price, "user_input")  # Источник: пользовательский ввод
        logging.info(f"Parsed product: name={name}, price={price}")
        await message.reply(f"✅ Найдено: {name} — {price} ₽")
    else:
        await message.reply("❌ Не удалось извлечь цену.")