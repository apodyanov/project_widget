"""Модуль функций-генераторов для обработки транзакционных данных."""


def filter_by_currency(transactions, currency_code):
    # Фильтрация транзакций по коду валюты с помощью генератора.
    for transaction in transactions:
        try:
            # Проверяем вложенную структуру operationAmount -> currency -> code
            operation_amount = transaction.get("operationAmount", {})
            currency = operation_amount.get("currency", {})
            if currency.get("code") == currency_code:
                yield transaction
        except (AttributeError, TypeError):
            # Пропускаем транзакции с некорректной структурой
            continue


def transaction_descriptions(transactions):
    # Извлечение описаний транзакций с помощью генератора
    for transaction in transactions:
        description = transaction.get("description")
        if description:  # Пропускаем транзакции без описания
            yield description


def card_number_generator(start, end):
    # Генерация номеров карт в диапазоне от начала до конца.
    if start < 1 or end > 9999999999999999:
        raise ValueError("Номер карты должен быть 0000000000000001 and 9999999999999999")

    if start > end:
        raise ValueError("Start должен быть меньше или эквивалентен end")

    for number in range(start, end + 1):
        # Форматируем число как 16-значную строку с ведущими нулями
        card_str = str(number).zfill(16)
        # Разбиваем на группы по 4 цифры
        formatted = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        yield formatted
