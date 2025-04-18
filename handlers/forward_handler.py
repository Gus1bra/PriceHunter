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
            # Определяем источник (название канала) и пользователя (кто переслал сообщение)
            source = message.forward_from_chat.title
            user = message.from_user.username or message.from_user.first_name
            
            # Обрабатываем каждый товар
            for name, price in results:
                # Проверяем типы данных перед записью в базу
                if not isinstance(name, str) or not isinstance(price, int):
                    raise ValueError("Некорректные данные: name должен быть строкой, price — целым числом.")
                
                # Добавляем товар в базу данных с указанием пользователя
                await insert_product(name, price, source, user)
                logging.info(f"✅ Добавлен товар: name={name}, price={price}, source={source}, user={user}")
            
            # Отправляем ответ пользователю
            await message.reply(f"✅ Найдено {len(results)} товар(ов). (Добавил: @{user})")
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
            # Определяем источник (пользовательский ввод) и пользователя (кто отправил сообщение)
            source = "user_input"
            user = message.from_user.username or message.from_user.first_name
            
            # Обрабатываем каждый товар
            for name, price in results:
                # Проверяем типы данных перед записью в базу
                if not isinstance(name, str) or not isinstance(price, int):
                    raise ValueError("Некорректные данные: name должен быть строкой, price — целым числом.")
                
                # Добавляем товар в базу данных с указанием пользователя
                await insert_product(name, price, source, user)
                logging.info(f"✅ Добавлен товар: name={name}, price={price}, source={source}, user={user}")
            
            # Отправляем ответ пользователю
            await message.reply(f"✅ Найдено {len(results)} товар(ов). (Добавил: @{user})")
        else:
            await message.reply("❌ Не удалось извлечь товары из текстового сообщения.")
    except Exception as e:
        logging.error(f"Ошибка при обработке текстового сообщения: {e}")
        await message.reply("❌ Произошла ошибка при обработке сообщения.")