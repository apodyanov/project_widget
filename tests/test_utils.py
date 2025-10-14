import pytest
import json
import tempfile
import os
from src.utils import load_transactions


class TestLoadTransactions:
    """Тесты для функции load_transactions"""

    def test_load_valid_transactions(self):
        """Тест загрузки валидного файла с транзакциями"""
        # Создаем тестовые данные
        test_data = [
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589"
            },
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "operationAmount": {
                    "amount": "8221.37",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560"
            }
        ]

        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            # Загружаем транзакции
            result = load_transactions(temp_path)

            # Проверяем результат
            assert result == test_data
            assert isinstance(result, list)
            assert len(result) == 2
        finally:
            # Удаляем временный файл
            os.unlink(temp_path)

    def test_file_not_found(self):
        """Тест для случая, когда файл не найден"""
        result = load_transactions("nonexistent_file.json")
        assert result == []
        assert isinstance(result, list)

    def test_empty_file(self):
        """Тест для пустого файла"""
        # Создаем пустой файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_invalid_json_format(self):
        """Тест для файла с невалидным JSON"""
        # Создаем файл с невалидным JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content {")
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_json_not_list(self):
        """Тест для случая, когда JSON содержит не список"""
        # Создаем файл с JSON объектом (не списком)
        test_data = {
            "transaction": {
                "id": 1,
                "amount": "100.0"
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_empty_list_in_file(self):
        """Тест для файла с пустым списком"""
        test_data = []

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == []
            assert isinstance(result, list)
        finally:
            os.unlink(temp_path)

    def test_file_with_only_whitespace(self):
        """Тест для файла содержащего только пробелы"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("   \n   \t   ")
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_large_transactions_list(self):
        """Тест загрузки большого списка транзакций"""
        # Создаем большой список транзакций
        large_data = [
            {
                "id": i,
                "state": "EXECUTED",
                "operationAmount": {
                    "amount": str(i * 100.0),
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": f"Транзакция {i}"
            }
            for i in range(100)
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(large_data, f)
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == large_data
            assert len(result) == 100
        finally:
            os.unlink(temp_path)

    def test_transactions_with_missing_fields(self):
        """Тест загрузки транзакций с отсутствующими полями"""
        test_data = [
            {
                "id": 1,
                # Нет поля 'state'
                "operationAmount": {
                    "amount": "100.0",
                    "currency": {
                        "code": "RUB"
                        # Нет поля 'name'
                    }
                }
                # Нет поля 'description'
            },
            {
                # Нет поля 'id'
                "state": "EXECUTED",
                "operationAmount": {
                    "amount": "200.0",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод"
            }
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == test_data
            assert len(result) == 2
        finally:
            os.unlink(temp_path)

    def test_special_characters_in_data(self):
        """Тест загрузки транзакций со специальными символами"""
        test_data = [
            {
                "id": 1,
                "description": "Платеж с спец. символами: !@#$%^&*()",
                "operationAmount": {
                    "amount": "1000.50",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                }
            }
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', encoding='utf-8', delete=False) as f:
            json.dump(test_data, f, ensure_ascii=False)
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == test_data
            assert "спец. символами" in result[0]["description"]
        finally:
            os.unlink(temp_path)


class TestLoadTransactionsEdgeCases:
    """Тесты для граничных случаев функции load_transactions"""

    def test_nonexistent_directory(self):
        """Тест для несуществующей директории"""
        result = load_transactions("nonexistent_dir/operations.json")
        assert result == []


    def test_very_large_file(self):
        """Тест для очень большого файла (в рамках разумного)"""
        # Создаем файл с большим количеством данных
        large_data = [{"id": i, "amount": str(i * 10)} for i in range(1000)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(large_data, f)
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert len(result) == 1000
            assert result == large_data
        finally:
            os.unlink(temp_path)


def test_load_transactions_return_type():
    """Тест, что функция всегда возвращает список"""
    # Тестируем различные случаи, чтобы убедиться, что всегда возвращается список

    # Случай с валидным файлом
    test_data = [{"id": 1}]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        result = load_transactions(temp_path)
        assert isinstance(result, list)
    finally:
        os.unlink(temp_path)

    # Случай с несуществующим файлом
    result = load_transactions("nonexistent.json")
    assert isinstance(result, list)

    # Случай с невалидным JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid")
        temp_path = f.name

    try:
        result = load_transactions(temp_path)
        assert isinstance(result, list)
    finally:
        os.unlink(temp_path)


# Дополнительные тесты для проверки корректности данных
class TestDataCorrectness:
    """Тесты корректности загруженных данных"""

    def test_data_structure_preserved(self):
        """Тест, что структура данных сохраняется правильно"""
        complex_data = [
            {
                "id": 123,
                "state": "EXECUTED",
                "date": "2023-01-01T12:00:00.000000",
                "operationAmount": {
                    "amount": "100.50",
                    "currency": {
                        "name": "US Dollar",
                        "code": "USD",
                        "symbol": "$"
                    }
                },
                "description": "Test transaction",
                "from": "Account 123",
                "to": "Account 456",
                "extra_field": "extra_value"
            }
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(complex_data, f)
            temp_path = f.name

        try:
            result = load_transactions(temp_path)

            # Проверяем, что все поля сохранились
            assert result[0]["id"] == 123
            assert result[0]["state"] == "EXECUTED"
            assert result[0]["operationAmount"]["amount"] == "100.50"
            assert result[0]["operationAmount"]["currency"]["code"] == "USD"
            assert result[0]["extra_field"] == "extra_value"

        finally:
            os.unlink(temp_path)