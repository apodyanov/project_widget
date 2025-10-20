import json
import logging
import os
from typing import Any, Dict, List

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", encoding="utf-8")
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

        logger.info("Вывод списка с данными о финансовых транзакциях")
        return data

    except (json.JSONDecodeError, PermissionError, OSError) as ex:
        logger.error("Произошла ошибка: %s", ex)
        return []
