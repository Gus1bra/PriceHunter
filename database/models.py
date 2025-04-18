import aiosqlite
from config import DB_PATH

# Добавление товара в базу данных
async def insert_product(name: str, price: int, source: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO products (name, price, source) VALUES (?, ?, ?)",
            (name, price, source)
        )
        await db.commit()

# Получение лучшего товара (с минимальной ценой)
async def get_best_product():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute('''
            SELECT name, price, source FROM products
            ORDER BY price ASC LIMIT 1
        ''')
        result = await cursor.fetchone()
        return result

# Получение последних N товаров
async def get_latest_products(n: int = 5):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute('''
            SELECT name, price, source FROM products
            ORDER BY created_at DESC LIMIT ?
        ''', (n,))
        results = await cursor.fetchall()
        return results