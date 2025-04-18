import re
from utils.text import normalize_price
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_product(text: str):
    """
    Извлекает товары и их цены из большого текста.
    Поддерживается запись в кавычках, перечисления через запятую и использование разделителей ':' или '-'.
    :param text: Входящий текст с информацией о товарах и ценах.
    :return: Список кортежей вида [(товар, цена)]
    """
    results = []
    
    # Разбиваем исходный текст на строки
    lines = text.splitlines()
    
    for line in lines:
        # Пропускаем пустые строки
        if not line.strip():
            continue
            
        # Ищем текст в кавычках
        matches = re.findall(r'"([^"]*)"', line)
        
        # Если ничего не найдено в кавычках, пытаемся обработать сам текст целиком
        if not matches:
            matches = [line]
        
        for item in matches:
            # Обрабатываем каждую найденную единицу товара
            # Ищем разделитель (- или :)
            separator_pos = max(item.find('-'), item.find(':'))
            
            if separator_pos >= 0:
                # Отделяем имя товара (до разделителя)
                product_name = item[:separator_pos].strip()
                
                # Отделяем цену (после разделителя)
                raw_price = item[separator_pos + 1:].strip().replace('₽', '').replace(',', '.')
                
                try:
                    # Приведение цены к числу
                    normalized_price = normalize_price(raw_price)
                    
                    # Сохраняем результат
                    results.append((product_name, normalized_price))
                    logger.info(f"✅ Успешно извлечён товар: {product_name}, цена: {normalized_price}")
                except ValueError as e:
                    logger.error(f"❌ Ошибка при нормализации цены для товара '{product_name}': {e}")
    
    return results