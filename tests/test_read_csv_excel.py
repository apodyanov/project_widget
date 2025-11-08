import pytest
import pandas as pd
import os
from unittest.mock import patch
import tempfile
from src.read_csv_excel import read_transactions_csv, read_transactions_excel


class TestReadTransactionsCSV:
    """Тесты для функции read_transactions_csv"""

    def test_read_csv_success(self, capsys):
        """Тест успешного чтения CSV файла"""
        # Создаем временный CSV файл
        csv_content = """дата,сумма,категория
2024-01-01,1000,продукты
2024-01-02,500,транспорт"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(csv_content)
            temp_file_path = f.name

        try:
            # Вызываем функцию
            read_transactions_csv(temp_file_path)

            # Проверяем вывод
            captured = capsys.readouterr()
            assert "Строка 1: ['дата', 'сумма', 'категория']" in captured.out
            assert "Строка 2: ['2024-01-01', '1000', 'продукты']" in captured.out
            assert "Строка 3: ['2024-01-02', '500', 'транспорт']" in captured.out

        finally:
            # Удаляем временный файл
            os.unlink(temp_file_path)

    def test_read_csv_file_not_found(self, capsys):
        """Тест обработки отсутствующего файла"""
        read_transactions_csv("nonexistent_file.csv")

        captured = capsys.readouterr()
        assert "Ошибка: Файл 'nonexistent_file.csv' не найден" in captured.out

    def test_read_csv_empty_file(self, capsys):
        """Тест чтения пустого CSV файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("")
            temp_file_path = f.name

        try:
            read_transactions_csv(temp_file_path)

            captured = capsys.readouterr()
            # Пустой файл должен вывести только заголовок (если есть) или ничего
            assert "Строка 1" in captured.out or captured.out == ""

        finally:
            os.unlink(temp_file_path)

    @patch('builtins.open')
    def test_read_csv_general_exception(self, mock_file, capsys):
        """Тест обработки общего исключения"""
        mock_file.side_effect = Exception("Test error")

        read_transactions_csv("any_file.csv")

        captured = capsys.readouterr()
        assert "Ошибка: Test error" in captured.out


class TestReadTransactionsExcel:
    """Тесты для функции read_transactions_excel"""

    def test_read_excel_success(self, capsys):
        """Тест успешного чтения Excel файла"""
        # Создаем тестовый DataFrame
        test_data = {
            'дата': ['2024-01-01', '2024-01-02'],
            'сумма': [1000, 500],
            'категория': ['продукты', 'транспорт']
        }
        df = pd.DataFrame(test_data)

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_file_path = f.name

        try:
            # Сохраняем DataFrame в Excel
            df.to_excel(temp_file_path, index=False)

            # Вызываем функцию
            read_transactions_excel(temp_file_path)

            # Проверяем вывод
            captured = capsys.readouterr()
            assert "Построчный вывод:" in captured.out
            assert "Строка 1:" in captured.out
            assert "Строка 2:" in captured.out
            assert "продукты" in captured.out
            assert "транспорт" in captured.out

        finally:
            os.unlink(temp_file_path)

    def test_read_excel_file_not_found(self, capsys):
        """Тест обработки отсутствующего Excel файла"""
        read_transactions_excel("nonexistent_file.xlsx")

        captured = capsys.readouterr()
        assert "Ошибка: Файл 'nonexistent_file.xlsx' не найден" in captured.out

    def test_read_excel_empty_dataframe(self, capsys):
        """Тест чтения Excel файла с пустыми данными"""
        # Создаем пустой DataFrame
        df = pd.DataFrame()

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_file_path = f.name

        try:
            df.to_excel(temp_file_path, index=False)
            read_transactions_excel(temp_file_path)

            captured = capsys.readouterr()
            assert "Построчный вывод:" in captured.out
            # Для пустого DataFrame не должно быть строк с данными

        finally:
            os.unlink(temp_file_path)

    @patch('pandas.read_excel')
    def test_read_excel_general_exception(self, mock_read_excel, capsys):
        """Тест обработки общего исключения при чтении Excel"""
        mock_read_excel.side_effect = Exception("Excel read error")

        read_transactions_excel("any_file.xlsx")

        captured = capsys.readouterr()
        assert "Ошибка: Excel read error" in captured.out

    def test_read_excel_with_different_encodings(self, capsys):
        """Тест чтения Excel с различными структурами данных"""
        test_data = {
            'ID': [1, 2, 3],
            'Amount': [100.50, 200.75, 300.25],
            'Description': ['Food', 'Transport', 'Entertainment']
        }
        df = pd.DataFrame(test_data)

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_file_path = f.name

        try:
            df.to_excel(temp_file_path, index=False)
            read_transactions_excel(temp_file_path)

            captured = capsys.readouterr()
            assert "Построчный вывод:" in captured.out
            assert "Строка 1:" in captured.out
            assert "Строка 2:" in captured.out
            assert "Строка 3:" in captured.out

        finally:
            os.unlink(temp_file_path)



# Фикстуры для тестов
@pytest.fixture
def sample_csv_file():
    """Фикстура для создания тестового CSV файла"""
    content = "name,age,city\nJohn,30,New York\nAlice,25,London"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write(content)
        temp_path = f.name

    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def sample_excel_file():
    """Фикстура для создания тестового Excel файла"""
    data = {
        'Product': ['Apple', 'Banana', 'Orange'],
        'Price': [1.2, 0.8, 1.5],
        'Quantity': [10, 15, 8]
    }
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        temp_path = f.name
        df.to_excel(temp_path, index=False)

    yield temp_path
    os.unlink(temp_path)
