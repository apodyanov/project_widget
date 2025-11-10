import csv
from typing import Any, Dict, Hashable, List

import pandas as pd

from config import TRANSACTIONS_CSV_FILE_PATH, TRANSACTIONS_EXCEL_FILE_PATH


def read_transactions_csv(file_path: str | None = None) -> List[Dict[str, Any]]:
    """
    Функция для чтения и вывода CSV файла
    """

    if file_path is None:
        file_path = TRANSACTIONS_CSV_FILE_PATH

    transactions = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Преобразуем OrderedDict в обычный dict и добавляем в список
                transactions.append(dict(row))  # type: ignore
        print(f"Успешно загружено {len(transactions)} транзакций из CSV файла")
        return transactions

    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден")
        return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []


def read_transactions_excel(file_path: str | None = None) -> list[dict[Hashable, Any]] | None:
    """
    Функция для чтения и вывода EXCEL файла
    """
    if file_path is None:
        file_path = TRANSACTIONS_EXCEL_FILE_PATH

    try:
        df = pd.read_excel(file_path)

        transactions = df.to_dict("records")

        print(f"Успешно загружено {len(transactions)} транзакций из Excel файла")
        return transactions

    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден")
        return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []
