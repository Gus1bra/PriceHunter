import aiosqlite
from config import DB_PATH

# Добавление товара в базу данных
async def insert_product(name: str, price: int, source: str):
    """
    Добавляет товар в базу данных.
    :param name: Название товара (строка)
    :param price: Цена товара (целое число)
    :param source: Источник товара (строка)
    """
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO products (name, price, source) VALUES (?, ?, ?)",
                (name, price, source)
            )
            await db.commit()
            print(f"✅ Товар '{name}' успешно добавлен в базу.")
    except Exception as e:
        raise RuntimeError(f"Ошибка при добавлении товара в базу: {e}")

# Получение лучшего товара (с минимальной ценой)
async def get_best_product():
    """
    Возвращает товар с минимальной ценой.
    :return: Кортеж (name, price, source) или None, если товаров нет
    """
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute('''
                SELECT name, price, source FROM products
                ORDER BY price ASC LIMIT 1
            ''')
            result = await cursor.fetchone()
            return result
    except Exception as e:
        raise RuntimeError(f"Ошибка при получении лучшего товара: {e}")

# Получение последних N товаров
async def get_latest_products(n: int = 5):
    """
    Возвращает последние N товаров, отсортированных по времени создания.
    :param n: Количество товаров (по умолчанию 5)
    :return: Список кортежей [(name, price, source), ...]
    """
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute('''
                SELECT name, price, source FROM products
                ORDER BY created_at DESC LIMIT ?
            ''', (n,))
            results = await cursor.fetchall()
            return results
    except Exception as e:
        raise RuntimeError(f"Ошибка при получении последних товаров: {e}")