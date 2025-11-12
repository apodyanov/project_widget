import json, random
import logging
import os
from typing import Any, Dict, List

from external_api import get_amount_in_rub

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s : %(name)s : %(levelname)s : %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях.

    Args:
        file_path (str): Путь до JSON-файла с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
                              Если файл пустой, содержит не список или не найден,
                              возвращает пустой список.
    """
    try:
        # Проверяем существование файла
        logger.info("Проверка существование файла")
        if not os.path.exists(file_path):
            logger.error("Файл не найден")
            return []

        # Проверяем, что файл не пустой
        logger.info("Проверка наличия данных в файле")
        if os.path.getsize(file_path) == 0:
            logger.error("Файл не содержит данных")
            return []

        # Читаем и парсим JSON файл
        logger.info("Считывание данных файла")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные - это список
        logger.info("Проверка на соответствие типа данных файла")
        if not isinstance(data, list):
            logger.error("Ошибка типа данных файла")
            return []

        logger.info("Вывод списка с данными")
        return data

    except (json.JSONDecodeError, PermissionError, OSError) as ex:
        logger.error("Произошла ошибка: %s", ex)
        return []


print('-'*50)
print('Домашнее задание 12.1 Библиотеки json, requests и datetime.')
print()
print('='*50)


def main():
    transactions = load_transactions("data/operations.json")
    print(f"Загружено транзакций: {len(transactions)}")
    print("\nСлучайная выборка 5 транзакций:")

    # Случайная выборка 5 транзакций
    if len(transactions) > 5:
        random_transactions = random.sample(transactions, 5)
    else:
        random_transactions = transactions

    # Обрабатываем случайные транзакции
    for i, transaction in enumerate(random_transactions, 1):
        amount_rub = get_amount_in_rub(transaction)

        operation_amount = transaction.get('operationAmount', {})
        original_amount = operation_amount.get('amount', '0')
        currency_code = operation_amount.get('currency', {}).get('code', 'RUB')
        description = transaction.get('description', 'Без описания')

        print(f"\nТранзакция {i}: {description}")
        print(f"  Сумма: {original_amount} {currency_code}")
        print(f"  В рублях: {amount_rub:.2f} RUB")