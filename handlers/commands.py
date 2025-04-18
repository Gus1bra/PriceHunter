from aiogram import Router
from aiogram.filters import Command 
from aiogram.types import Message
from database.models import get_best_product, get_latest_products

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Привет! Перешли сюда пост с товаром, и я помогу найти лучшую цену.")

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "/start — запуск\n"
        "/best — лучший товар\n"
        "/last — последние товары"
    )

@router.message(Command("best"))
async def best_cmd(message: Message):
    best_product = await get_best_product()
    if best_product:
        name, price, source = best_product
        await message.answer(f"🏆 Лучший товар:\n{name} — {price} ₽\nИсточник: {source}")
    else:
        await message.answer("❌ Нет данных о товарах.")

@router.message(Command("last"))
async def last_cmd(message: Message):
    latest_products = await get_latest_products(5)  # Последние 5 товаров
    if latest_products:
        response = "🕒 Последние товары:\n"
        for product in latest_products:
            name, price, source = product
            response += f"{name} — {price} ₽ (Источник: {source})\n"
        await message.answer(response)
    else:
        await message.answer("❌ Нет данных о товарах.")