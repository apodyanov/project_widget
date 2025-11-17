from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.read_json_csv_excel import read_transactions_csv, read_transactions_excel


class TestReadTransactionsCSV:
    """Тесты для функции read_transactions_csv"""

    def test_read_valid_csv_with_headers(self) -> None:
        """Тест чтения корректного CSV файла с заголовками"""
        csv_content = """date,amount,description,category
2023-01-01,1000.00,Salary,Income
2023-01-02,-500.50,Groceries,Food
2023-01-03,-45.00,Transport,Transportation"""

        expected = [
            {"date": "2023-01-01", "amount": "1000.00", "description": "Salary", "category": "Income"},
            {"date": "2023-01-02", "amount": "-500.50", "description": "Groceries", "category": "Food"},
            {"date": "2023-01-03", "amount": "-45.00", "description": "Transport", "category": "Transportation"},
        ]

        with patch("builtins.open", mock_open(read_data=csv_content)):
            result = read_transactions_csv("test.csv")

        assert result == expected
        assert len(result) == 3
        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)

    def test_read_empty_csv(self) -> None:
        """Тест чтения пустого CSV файла"""
        csv_content = "date,amount,description\n"

        with patch("builtins.open", mock_open(read_data=csv_content)):
            result = read_transactions_csv("empty.csv")

        assert result == []
        assert isinstance(result, list)

    def test_read_csv_only_headers(self) -> None:
        """Тест чтения CSV только с заголовками без данных"""
        csv_content = "date,amount,description,category\n"

        with patch("builtins.open", mock_open(read_data=csv_content)):
            result = read_transactions_csv("headers_only.csv")

        assert result == []
        assert isinstance(result, list)

    def test_file_not_found_csv(self) -> None:
        """Тест обработки отсутствующего CSV файла"""
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            result = read_transactions_csv("nonexistent.csv")

        assert result == []
        assert isinstance(result, list)

    def test_csv_reading_exception(self) -> None:
        """Тест обработки исключений при чтении CSV"""
        with patch("builtins.open", side_effect=Exception("Read error")):
            result = read_transactions_csv("corrupted.csv")

        assert result == []
        assert isinstance(result, list)


class TestReadTransactionsExcel:
    """Тесты для функции read_transactions_excel"""

    def test_read_valid_excel(self) -> None:
        """Тест чтения корректного Excel файла"""
        mock_data = {
            "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "amount": [1000.00, -500.50, -45.00],
            "description": ["Salary", "Groceries", "Transport"],
            "category": ["Income", "Food", "Transportation"],
        }
        mock_df = pd.DataFrame(mock_data)

        expected = [
            {"date": "2023-01-01", "amount": 1000.00, "description": "Salary", "category": "Income"},
            {"date": "2023-01-02", "amount": -500.50, "description": "Groceries", "category": "Food"},
            {"date": "2023-01-03", "amount": -45.00, "description": "Transport", "category": "Transportation"},
        ]

        with patch("pandas.read_excel", return_value=mock_df):
            result = read_transactions_excel("test.xlsx")

        assert result == expected
        assert len(result) == 3
        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)

    def test_read_empty_excel(self) -> None:
        """Тест чтения пустого Excel файла"""
        mock_df = pd.DataFrame()

        with patch("pandas.read_excel", return_value=mock_df):
            result = read_transactions_excel("empty.xlsx")

        assert result == []
        assert isinstance(result, list)

    def test_file_not_found_excel(self) -> None:
        """Тест обработки отсутствующего Excel файла"""
        with patch("pandas.read_excel", side_effect=FileNotFoundError("File not found")):
            result = read_transactions_excel("nonexistent.xlsx")

        assert result == []
        assert isinstance(result, list)

    def test_excel_reading_exception(self) -> None:
        """Тест обработки исключений при чтении Excel"""
        with patch("pandas.read_excel", side_effect=Exception("Excel read error")):
            result = read_transactions_excel("corrupted.xlsx")

        assert result == []
        assert isinstance(result, list)


class TestIntegration:
    """Интеграционные тесты для проверки взаимодействия"""

    def test_both_functions_return_lists(self) -> None:
        """Тест, что обе функции всегда возвращают списки"""
        # Даже при ошибках функции должны возвращать списки
        with patch("builtins.open", side_effect=FileNotFoundError()):
            csv_result = read_transactions_csv("nonexistent.csv")

        with patch("pandas.read_excel", side_effect=FileNotFoundError()):
            excel_result = read_transactions_excel("nonexistent.xlsx")

        assert isinstance(csv_result, list)
        assert isinstance(excel_result, list)

    def test_transactions_structure(self) -> None:
        """Тест структуры возвращаемых транзакций"""
        csv_content = """date,amount,description
2023-01-01,1000.00,Salary"""

        with patch("builtins.open", mock_open(read_data=csv_content)):
            transactions = read_transactions_csv("test.csv")

        # Проверяем структуру первой транзакции
        if transactions:
            first_transaction = transactions[0]
            assert isinstance(first_transaction, dict)
            assert "date" in first_transaction
            assert "amount" in first_transaction
            assert "description" in first_transaction

    @pytest.mark.parametrize("file_path", [None, "custom_path.csv"])
    def test_default_file_path(self, file_path: str) -> None:
        """Тест работы с default file path"""
        csv_content = "date,amount,description\n2023-01-01,1000,Salary"

        with patch("builtins.open", mock_open(read_data=csv_content)):
            with patch("src.read_csv_excel.TRANSACTIONS_CSV_FILE_PATH", "default.csv"):
                if file_path is None:
                    result = read_transactions_csv()
                else:
                    result = read_transactions_csv(file_path)

        assert isinstance(result, list)


# Тесты для проверки конкретных сценариев из финансового приложения
class TestFinancialScenarios:
    """Тесты для финансовых сценариев"""

    def test_bank_statement_format(self) -> None:
        """Тест формата банковской выписки"""
        bank_statement_content = """Дата операции,Сумма,Категория,Описание
2024-01-15,1500.00,Доход,Зарплата
2024-01-16,-250.50,Продукты,Супермаркет
2024-01-17,-45.00,Транспорт,Метро"""

        expected = [
            {"Дата операции": "2024-01-15", "Сумма": "1500.00", "Категория": "Доход", "Описание": "Зарплата"},
            {"Дата операции": "2024-01-16", "Сумма": "-250.50", "Категория": "Продукты", "Описание": "Супермаркет"},
            {"Дата операции": "2024-01-17", "Сумма": "-45.00", "Категория": "Транспорт", "Описание": "Метро"},
        ]

        with patch("builtins.open", mock_open(read_data=bank_statement_content)):
            result = read_transactions_csv("bank_statement.csv")

        assert result == expected
