# test_parser.py
from services.parser import extract_product

test_messages = [
    "Xiaomi Redmi Note 10S - 25 000 ₽",
    "🔥 Huawei P50 Pro - 80 000 ₽",
    "Acer Aspire V15 Nitro: 45 000 ₽"
]

for message in test_messages:
    result = extract_product(message)
    print(f"Input: {message} -> Output: {result}")