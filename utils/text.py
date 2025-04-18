def normalize_price(raw_price: str) -> int:
    """
    Нормализует строку с ценой в целое число.
    :param raw_price: Строка с ценой (например, "70 000 ₽").
    :return: Целое число (например, 70000).
    """
    # Удаляем все символы, кроме цифр и пробелов
    cleaned_price = ''.join(filter(lambda x: x.isdigit() or x.isspace(), raw_price))
    # Преобразуем в целое число
    return int("".join(cleaned_price.split()))