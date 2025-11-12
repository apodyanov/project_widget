"""Главный модуль запуска программы."""
from config import TRANSACTIONS_CSV_FILE_PATH, TRANSACTIONS_EXCEL_FILE_PATH

from src.read_csv_excel import read_transactions_csv, read_transactions_excel


if __name__ == "__main__":
    pass










print('-'*50)
print('Домашнее задание 13.1 Библиотеки csv и pandas')
print()
print('='*50)

print("\nФункция для чтения и вывода CSV файла")
print("-" * 30)
read_transactions_csv(TRANSACTIONS_CSV_FILE_PATH)
print("\nФункция для чтения и вывода EXCEL файла")
print("-" * 30)
read_transactions_excel(TRANSACTIONS_EXCEL_FILE_PATH)



