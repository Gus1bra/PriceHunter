from aiogram import Router, F
from aiogram.types import Message
from services.parser import extract_product
from database.models import insert_product
import logging

# Инициализация роутера
router = Router()

@router.message(F.forward_from_chat)
async def handle_forward(message: Message):
    """
    Обрабатывает пересланные сообщения из каналов.
    """
    try:
        # Извлекаем данные о товарах из текста
        results = extract_product(message.text)
        if results:
            for name, price in results:  # Обрабатываем каждый товар
                source = message.forward_from_chat.title  # Источник: название канала
                # Проверяем типы данных перед записью в базу
                if not isinstance(name, str) or not isinstance(price, int):
                    raise ValueError("Некорректные данные: name должен быть строкой, price — целым числом.")
                
                # Добавляем товар в базу данных
                await insert_product(name, price, source)
                logging.info(f"✅ Добавлен товар: name={name}, price={price}, source={source}")
            
            # Отправляем ответ пользователю
            await message.reply(f"✅ Найдено {len(results)} товар(ов).")
        else:
            await message.reply("❌ Не удалось извлечь товары из пересланного сообщения.")
    except Exception as e:
        logging.error(f"Ошибка при обработке пересланного сообщения: {e}")
        await message.reply("❌ Произошла ошибка при обработке сообщения.")

@router.message(F.text)  # Обработка обычных текстовых сообщений
async def handle_text(message: Message):
    """
    Обрабатывает обычные текстовые сообщения от пользователей.
    """
    try:
        # Извлекаем данные о товарах из текста
        results = extract_product(message.text)
        if results:
            for name, price in results:  # Обрабатываем каждый товар
                source = "user_input"  # Источник: пользовательский ввод
                # Проверяем типы данных перед записью в базу
                if not isinstance(name, str) or not isinstance(price, int):
                    raise ValueError("Некорректные данные: name должен быть строкой, price — целым числом.")
                
                # Добавляем товар в базу данных
                await insert_product(name, price, source)
                logging.info(f"✅ Добавлен товар: name={name}, price={price}, source={source}")
            
            # Отправляем ответ пользователю
            await message.reply(f"✅ Найдено {len(results)} товар(ов).")
        else:
            await message.reply("❌ Не удалось извлечь товары из текстового сообщения.")
    except Exception as e:
        logging.error(f"Ошибка при обработке текстового сообщения: {e}")
        await message.reply("❌ Произошла ошибка при обработке сообщения.")