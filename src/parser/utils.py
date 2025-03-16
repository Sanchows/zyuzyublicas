import re


def clean_price(price: str) -> float:
    # Убираем все символы, кроме цифр, запятых и точек
    price = re.sub(r'[^\d,.]', '', price)

    # Заменяем запятую на точку, если она используется как десятичный разделитель
    if ',' in price and '.' in price:
        price = price.replace('.', '')  # Убираем точку, если есть запятая
    price = price.replace(',', '.')  # Заменяем запятую на точку

    price = re.sub(r'\.+$', '', price)  # Убираем точки в конце
    price = re.sub(r'[^\d.]', '', price)  # Убираем лишние символы

    return float(price)


def get_avg_price(prices: list[float | int]) -> float:
    if len(prices) == 0:
        return 0.0
    return sum(map(lambda x: x*100, prices)) / len(prices) / 100.0
