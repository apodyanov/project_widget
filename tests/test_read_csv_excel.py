from typing import List, Dict, Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.read_json_csv_excel import read_transactions_csv, read_transactions_excel, FileReadError


@pytest.fixture
def sample_csv_content() -> str:
    """Фикстура с корректным CSV содержимым"""
    return """id;state;date;amount;currency_name;currency_code;from;to;description
650703;EXECUTED;2023-09-05T11:30:32Z;16210.0;Sol;PEN;Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации
441945;EXECUTED;2019-08-26T10:50:58Z;31957.58;руб.;RUB;Maestro 1596837868705199;Счет 64686473678894779589;Перевод организации
"""


@pytest.fixture
def sample_excel_data() -> List[Dict[str, Any]]:
    """Фикстура с корректными данными для Excel"""
    return [
        {
            'id': 650703,
            'state': 'EXECUTED',
            'date': '2023-09-05T11:30:32Z',
            'amount': 16210.0,
            'currency_name': 'Sol',
            'currency_code': 'PEN',
            'from': 'Счет 58803664561298323391',
            'to': 'Счет 39745660563456619397',
            'description': 'Перевод организации'
        }
    ]


@pytest.fixture
def temp_csv_file(tmp_path, sample_csv_content):
    """Создает временный CSV файл для тестов"""
    csv_file = tmp_path / "test_transactions.csv"
    csv_file.write_text(sample_csv_content, encoding='utf-8')
    return csv_file


@pytest.fixture
def temp_excel_file(tmp_path, sample_excel_data):
    """Создает временный Excel файл для тестов"""
    excel_file = tmp_path / "test_transactions.xlsx"
    df = pd.DataFrame(sample_excel_data)
    df.to_excel(excel_file, index=False)
    return excel_file



class TestReadTransactionsCSV:
    """Тесты для функции read_transactions_csv"""

    def test_read_valid_csv_with_headers(self, temp_csv_file):
        """Тест чтения корректного CSV файла"""
        result = read_transactions_csv(str(temp_csv_file))

        assert len(result) == 2
        assert result[0]['id'] == '650703'
        assert result[0]['state'] == 'EXECUTED'
        assert result[0]['operationAmount']['amount'] == '16210.0'
        assert result[0]['operationAmount']['currency']['code'] == 'PEN'

    def test_file_not_found_csv(self):
        """Тест обработки отсутствующего CSV файла"""
        with pytest.raises(FileReadError, match="Файл .* не найден"):
            read_transactions_csv("nonexistent.csv")

    def test_csv_with_missing_required_field(self, tmp_path):
        """Тест CSV с отсутствующим обязательным полем"""
        # Создаем CSV без поля 'id'
        bad_csv_content = """state;date;amount;currency_name;currency_code;from;to;description
EXECUTED;2023-09-05T11:30:32Z;16210.0;Sol;PEN;Счет 123;Счет 456;Перевод
"""
        csv_file = tmp_path / "bad.csv"
        csv_file.write_text(bad_csv_content, encoding='utf-8')

        with pytest.raises(FileReadError, match="Отсутствует обязательное поле"):
            read_transactions_csv(str(csv_file))

    def test_csv_reading_exception(self):
        """Тест обработки исключений при чтении CSV"""
        with patch('builtins.open', side_effect=Exception("Read error")):
            with pytest.raises(FileReadError, match="Ошибка при чтении CSV файла"):
                read_transactions_csv("test.csv")


class TestReadTransactionsExcel:
    """Тесты для функции read_transactions_excel"""

    def test_read_valid_excel(self, temp_excel_file):
        """Тест чтения корректного Excel файла"""
        result = read_transactions_excel(str(temp_excel_file))

        assert len(result) == 1
        assert result[0]['id'] == '650703'
        assert result[0]['state'] == 'EXECUTED'
        assert result[0]['operationAmount']['amount'] == '16210'
        assert result[0]['operationAmount']['currency']['code'] == 'PEN'

    def test_file_not_found_excel(self):
        """Тест обработки отсутствующего Excel файла"""
        with pytest.raises(FileReadError, match="Файл .* не найден"):
            read_transactions_excel("nonexistent.xlsx")

    def test_excel_with_missing_required_field(self, tmp_path):
        """Тест Excel с отсутствующим обязательным полем"""
        # Создаем DataFrame без поля 'id'
        bad_data = [{
            'state': 'EXECUTED',
            'date': '2023-09-05T11:30:32Z',
            'amount': 16210.0,
            'currency_name': 'Sol',
            'currency_code': 'PEN',
            'from': 'Счет 123',
            'to': 'Счет 456',
            'description': 'Перевод организации'
        }]

        excel_file = tmp_path / "bad.xlsx"
        df = pd.DataFrame(bad_data)
        df.to_excel(excel_file, index=False)

        with pytest.raises(FileReadError, match="Отсутствует обязательное поле"):
            read_transactions_excel(str(excel_file))

    def test_excel_reading_exception(self):
        """Тест обработки исключений при чтении Excel"""
        with patch('pandas.read_excel', side_effect=Exception("Excel read error")):
            with pytest.raises(FileReadError, match="Ошибка при чтении Excel файла"):
                read_transactions_excel("test.xlsx")


class TestIntegration:
    """Интеграционные тесты"""

    def test_both_functions_return_lists(self, temp_csv_file, temp_excel_file):
        """Тест, что обе функции возвращают списки"""
        csv_result = read_transactions_csv(str(temp_csv_file))
        excel_result = read_transactions_excel(str(temp_excel_file))

        assert isinstance(csv_result, list)
        assert isinstance(excel_result, list)

    def test_transactions_structure(self, temp_csv_file):
        """Тест структуры возвращаемых транзакций"""
        result = read_transactions_csv(str(temp_csv_file))
        transaction = result[0]

        # Проверяем обязательные поля
        assert 'id' in transaction
        assert 'state' in transaction
        assert 'date' in transaction
        assert 'operationAmount' in transaction
        assert 'description' in transaction

        # Проверяем вложенную структуру
        assert 'amount' in transaction['operationAmount']
        assert 'currency' in transaction['operationAmount']
        assert 'code' in transaction['operationAmount']['currency']


# Тесты для проверки конкретных сценариев из финансового приложения
class TestFinancialScenarios:
    """Тесты для финансовых сценариев"""

    def test_bank_statement_format(self, temp_csv_file):
        """Тест формата банковской выписки"""
        transactions = read_transactions_csv(str(temp_csv_file))

        for transaction in transactions:
            # Проверяем что все суммы положительные
            amount = float(transaction['operationAmount']['amount'])
            assert amount > 0

            # Проверяем валидность статусов
            assert transaction['state'] in ['EXECUTED', 'CANCELED', 'PENDING']

            # Проверяем что описания не пустые
            assert transaction['description'].strip() != ""
