import json
import os
from typing import List, Dict, Any


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.

    Args:
        file_path (str): Путь до JSON-файла с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
                              Если файл пустой, содержит не список или не найден,
                              возвращает пустой список.
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            return []

        # Проверяем, что файл не пустой
        if os.path.getsize(file_path) == 0:
            return []

        # Читаем и парсим JSON файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные - это список
        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, PermissionError, OSError):
        return []

