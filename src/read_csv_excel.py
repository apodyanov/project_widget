import csv

import pandas as pd

from config import TRANSACTIONS_CSV_FILE_PATH, TRANSACTIONS_EXCEL_FILE_PATH


def read_transactions_csv(file_path: str) -> None:
    """
    Функция для чтения и вывода CSV файла
    """
    file_path = TRANSACTIONS_CSV_FILE_PATH

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row_num, row in enumerate(reader, start=1):
                print(f"Строка {row_num}: {row}")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден")
    except Exception as e:
        print(f"Ошибка: {e}")


def read_transactions_excel(file_path: str) -> None:
    """
    Функция для чтения и вывода EXCEL файла
    """
    file_path = TRANSACTIONS_EXCEL_FILE_PATH

    try:
        df = pd.read_excel(file_path)

        print("\nПострочный вывод:")
        for row_num, row in df.iterrows():
            print(f"Строка {row_num + 1}: {row.to_dict()}") # type: ignore

    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден")
    except Exception as e:
        print(f"Ошибка: {e}")
