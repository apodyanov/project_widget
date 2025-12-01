import csv, os, json
from typing import Any, Dict, List

import pandas as pd

from config import TRANSACTIONS_CSV_FILE_PATH, TRANSACTIONS_EXCEL_FILE_PATH, TRANSACTIONS_JSON_FILE_PATH


class FileLoadError(Exception):
    """Пользовательское исключение для ошибок загрузки файлов"""
    pass

class FileReadError(Exception):
    """Пользовательское исключение для ошибок чтения файлов"""
    pass


def read_transactions_csv(file_path: str | None = None) -> List[Dict[str, Any]]:
    """
    Функция для чтения и вывода CSV файла
    """

    if file_path is None:
        file_path = TRANSACTIONS_CSV_FILE_PATH

    transactions = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Читаем CSV файл с разделителем;
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                # Преобразуем строку CSV в структуру, аналогичную JSON
                transaction = {
                    'id': str(row['id']),
                    'state': row['state'],
                    'date': row['date'],
                    'operationAmount': {
                        'amount': row['amount'],
                        'currency': {
                            'name': row['currency_name'],
                            'code': row['currency_code']
                        }
                    },
                    'description': row['description'],
                    'from': row['from'],
                    'to': row['to']
                }
                transactions.append(transaction)

    except FileNotFoundError:
        raise FileReadError(f"Файл {file_path} не найден")
    except KeyError as e:
        raise FileReadError(f"Отсутствует обязательное поле в CSV файле: {e}")
    except ValueError as e:
        raise FileReadError(f"Ошибка преобразования данных: {e}")
    except Exception as e:
        raise FileReadError(f"Ошибка при чтении CSV файла: {e}")

    return transactions


def read_transactions_excel(file_path: str | None = None) -> List[Dict[str, Any]]:
    """
    Функция для чтения Excel файла с транзакциями
    с улучшенной обработкой структуры данных
    """
    if file_path is None:
        file_path = TRANSACTIONS_EXCEL_FILE_PATH

    try:
        # Читаем Excel файл
        df = pd.read_excel(file_path)

        # Преобразуем DataFrame в список словарей
        transactions = []

        for _, row in df.iterrows():
            # Преобразуем строку Excel в структуру, аналогичную JSON
            transaction = {
                'id': str(row['id']),
                'state': str(row['state']),
                'date': str(row['date']),
                'operationAmount': {
                    'amount': str(row['amount']),
                    'currency': {
                        'name': str(row['currency_name']),
                        'code': str(row['currency_code'])
                    }
                },
                'description': str(row['description']),
                'from': str(row['from']),
                'to': str(row['to'])
            }
            transactions.append(transaction)

        return transactions

    except FileNotFoundError:
        raise FileReadError(f"Файл {file_path} не найден")
    except KeyError as e:
        raise FileReadError(f"Отсутствует обязательное поле в Excel файле: {e}")
    except ValueError as e:
        raise FileReadError(f"Ошибка преобразования данных: {e}")
    except Exception as e:
        raise FileReadError(f"Ошибка при чтении Excel файла: {e}")


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Функция для чтения и вывода json файла.

    Args:
        file_path (str): Путь до JSON-файла с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
                              Если файл пустой, содержит не список или не найден,
                              возвращает пустой список.
    """
    if file_path is None:
        file_path = TRANSACTIONS_JSON_FILE_PATH

    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            return []

        # Проверяем, что файл не пустой
        if os.path.getsize(file_path) == 0:
            return []

        # Читаем и парсим JSON файл
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные - это список
        if not isinstance(data, list):
            return []

        return data


    except json.JSONDecodeError as e:
        raise FileLoadError(f"Invalid JSON format: {e}")
    except PermissionError as e:
        raise FileLoadError(f"Permission denied: {e}")
    except OSError as e:
        raise FileLoadError(f"OS error: {e}")
