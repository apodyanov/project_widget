from typing import Any
from unittest.mock import patch

import pytest

# Импортируем функции для тестирования
from src.final_modul import (
    analyze_available_statuses,
    extract_categories_from_transactions,
    filter_rub_transactions,
    format_account_display,
    format_transaction_display,
    get_search_suggestions,
    get_status_input_with_suggestions,
    get_user_choice,
    handle_empty_status_filter,
    process_bank_operations,
    process_bank_search,
    sort_by_date,
)


class TestProcessBankSearch:
    """Тесты для функции process_bank_search"""

    def test_empty_data(self):
        """Тест с пустыми данными"""
        assert process_bank_search([], "test") == []

    def test_empty_search_string(self):
        """Тест с пустой строкой поиска"""
        data = [{"id": 1, "description": "test"}]
        assert process_bank_search(data, "") == []

    def test_basic_search(self):
        """Тест базового поиска"""
        data = [
            {"id": 1, "description": "Перевод организации", "state": "EXECUTED"},
            {"id": 2, "description": "Оплата услуг", "state": "CANCELED"},
            {"id": 3, "description": "Перевод карта", "state": "PENDING"},
        ]

        result = process_bank_search(data, "перевод")
        assert len(result) == 2
        assert all("перевод" in transaction["description"].lower() for transaction in result)

    def test_case_insensitive_search(self):
        """Тест поиска без учета регистра"""
        data = [
            {"id": 1, "description": "Перевод Организации", "state": "EXECUTED"},
            {"id": 2, "description": "перевод карта", "state": "PENDING"},
        ]

        result = process_bank_search(data, "ПЕРЕВОД")
        assert len(result) == 2

    def test_search_in_different_fields(self):
        """Тест поиска в разных полях"""
        data = [
            {"id": 1, "description": "Оплата", "state": "EXECUTED"},
            {"id": 2, "description": "Перевод", "state": "CANCELED"},
            {"id": 3, "description": "Пополнение", "state": "PENDING", "from": "Карта 1234567812345678"},
        ]

        result = process_bank_search(data, "12345678")
        assert len(result) == 1
        assert result[0]["id"] == 3

    def test_search_with_special_characters(self):
        """Тест поиска со специальными символами"""
        data = [{"id": 1, "description": "Payment (invoice #123)", "state": "EXECUTED"}]

        result = process_bank_search(data, "(invoice")
        assert len(result) == 1


class TestProcessBankOperations:
    """Тесты для функции process_bank_operations"""

    def test_empty_data(self):
        """Тест с пустыми данными"""
        assert process_bank_operations([], ["категория"]) == {}

    def test_empty_categories(self):
        """Тест с пустыми категориями"""
        data = [{"description": "Перевод организации"}]
        assert process_bank_operations(data, []) == {}

    def test_basic_category_counting(self):
        """Тест базового подсчета категорий"""
        data = [
            {"description": "Перевод организации"},
            {"description": "Перевод карта"},
            {"description": "Оплата услуг"},
            {"description": "Перевод организации"},
            {"description": "Пополнение счета"},
        ]

        categories = ["Перевод организации", "Оплата услуг"]
        result = process_bank_operations(data, categories)

        assert result == {"Перевод организации": 2, "Оплата услуг": 1}

    def test_case_insensitive_matching(self):
        """Тест сопоставления без учета регистра"""
        data = [
            {"description": "ПЕРЕВОД ОРГАНИЗАЦИИ"},
            {"description": "перевод карта"},
            {"description": "Оплата Услуг"},
        ]

        categories = ["Перевод организации", "оплата услуг"]
        result = process_bank_operations(data, categories)

        assert "Перевод организации" in result
        assert "оплата услуг" in result

    def test_partial_matching(self):
        """Тест частичного совпадения"""
        data = [
            {"description": "Перевод организации Сбербанк"},
            {"description": "Перевод организации Альфа-Банк"},
            {"description": "Оплата интернет услуг"},
        ]

        categories = ["Перевод организации", "Оплата"]
        result = process_bank_operations(data, categories)

        assert result["Перевод организации"] == 2
        assert result["Оплата"] == 1

    def test_no_matches(self):
        """Тест когда нет совпадений"""
        data = [{"description": "Пополнение счета"}, {"description": "Снятие наличных"}]

        categories = ["Перевод организации", "Оплата услуг"]
        result = process_bank_operations(data, categories)

        assert result == {}


class TestFormatAccountDisplay:
    """Тесты для функции format_account_display"""

    def test_empty_input(self):
        """Тест с пустым вводом"""
        assert format_account_display("") == "Не указано"

    def test_account_formatting(self):
        """Тест форматирования счета"""
        account_info = "Счет 12345678901234567890"
        result = format_account_display(account_info)
        assert "Счет" in result
        assert "**7890" in result

    def test_card_formatting(self):
        """Тест форматирования карты"""
        card_info = "Visa Platinum 1234567812345678"
        result = format_account_display(card_info)
        assert "Visa Platinum" in result
        assert "1234" in result  # Начало номера видно
        assert "5678" in result  # Конец номера видно

    def test_unknown_format(self):
        """Тест с неизвестным форматом"""
        unknown_info = "Неизвестный формат"
        result = format_account_display(unknown_info)
        assert result == "Неизвестный формат"


class TestFormatTransactionDisplay:
    """Тесты для функции format_transaction_display"""

    def test_basic_transaction_formatting(self):
        """Тест базового форматирования транзакции"""
        transaction = {
            "date": "2023-09-05T11:30:32Z",
            "description": "Перевод организации",
            "from": "Счет 12345678901234567890",
            "to": "Карта 1234567812345678",
            "operationAmount": {"amount": "16210.50", "currency": {"code": "RUB", "name": "руб."}},
        }

        result = format_transaction_display(transaction)

        assert "2023-09-05" in result
        assert "Перевод организации" in result
        assert "Счет" in result
        assert "16210.50" in result
        assert "RUB" in result
        assert "руб." in result

    def test_transaction_with_missing_fields(self):
        """Тест транзакции с отсутствующими полями"""
        transaction = {
            "date": "2023-09-05T11:30:32Z",
            "description": "Перевод",
            "operationAmount": {"amount": "1000", "currency": {"code": "USD"}},
        }

        result = format_transaction_display(transaction)
        assert "2023-09-05" in result
        assert "Перевод" in result
        assert "1000" in result
        assert "USD" in result


class TestGetUserChoice:
    """Тесты для функции get_user_choice"""

    @patch("builtins.input", return_value="1")
    def test_valid_choices_numeric(self, mock_input: Any) -> None:
        """Тест числовых валидных выборов"""
        result = get_user_choice("Выберите: ", ["1", "2", "3"])
        assert result == "1"

    @patch("builtins.input", return_value="да")
    def test_valid_choices_text(self, mock_input: Any) -> None:
        """Тест текстовых валидных выборов"""
        result = get_user_choice("Выберите: ", ["да", "нет"])
        assert result == "да"

    @patch("builtins.input", side_effect=["invalid", "5", "2"])
    def test_invalid_choices_retry(self, mock_input: Any) -> None:
        """Тест повторных попыток при невалидном вводе"""
        result = get_user_choice("Выберите: ", ["1", "2", "3"])
        assert result == "2"


class TestSortByDate:
    """Тесты для функции sort_by_date"""

    def test_empty_data(self):
        """Тест с пустыми данными"""
        assert sort_by_date([]) == []
        assert sort_by_date([], reverse=True) == []

    def test_basic_sorting(self):
        """Тест базовой сортировки"""
        data = [
            {"date": "2023-09-05T11:30:32Z", "id": 3},
            {"date": "2023-08-01T10:15:00Z", "id": 1},
            {"date": "2023-09-01T09:00:00Z", "id": 2},
        ]

        # Сортировка по возрастанию
        result_asc = sort_by_date(data)
        assert [t["id"] for t in result_asc] == [1, 2, 3]

        # Сортировка по убыванию
        result_desc = sort_by_date(data, reverse=True)
        assert [t["id"] for t in result_desc] == [3, 2, 1]

    def test_transactions_without_dates(self):
        """Тест транзакций без дат"""
        data = [
            {"date": "2023-09-05T11:30:32Z", "id": 2},
            {"date": None, "id": 1},
            {"date": "2023-09-01T09:00:00Z", "id": 3},
            {"date": "None", "id": 4},
        ]

        result = sort_by_date(data)
        # Должны остаться только транзакции с валидными датами
        assert len(result) == 2
        assert all(t["id"] in [2, 3] for t in result)


class TestFilterRubTransactions:
    """Тесты для функции filter_rub_transactions"""

    def test_empty_data(self):
        """Тест с пустыми данными"""
        assert filter_rub_transactions([]) == []

    def test_rub_filtering(self):
        """Тест фильтрации рублевых транзакций"""
        data = [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
            {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
            {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}},
        ]

        result = filter_rub_transactions(data)
        assert len(result) == 2
        assert all(t["id"] in [1, 3] for t in result)

    def test_invalid_currency_structure(self):
        """Тест с некорректной структурой валюты"""
        data = [{"id": 1, "operationAmount": "invalid"}, {"id": 2, "operationAmount": {"currency": "invalid"}}]

        result = filter_rub_transactions(data)
        assert len(result) == 0


class TestGetSearchSuggestions:
    """Тесты для функции get_search_suggestions"""

    def test_empty_data(self):
        """Тест с пустыми данными"""
        assert get_search_suggestions([]) == []

    def test_suggestions_generation(self):
        """Тест генерации подсказок"""
        data = [
            {"description": "Перевод организации Сбербанк"},
            {"description": "Перевод карты ВТБ"},
            {"description": "Оплата услуг интернет"},
            {"description": "Оплата мобильной связи"},
            {"description": "Перевод между счетами"},
        ]

        suggestions = get_search_suggestions(data)

        # Проверяем что подсказки не пустые
        assert len(suggestions) > 0
        # Проверяем что служебные слова отфильтрованы
        assert "и" not in suggestions
        assert "в" not in suggestions


class TestAnalyzeAvailableStatuses:
    """Тесты для функции analyze_available_statuses"""

    def test_empty_data(self):
        """Тест с пустыми данными"""
        assert analyze_available_statuses([]) == {}

    def test_status_analysis(self):
        """Тест анализа статусов"""
        data = [
            {"state": "EXECUTED"},
            {"state": "CANCELED"},
            {"state": "EXECUTED"},
            {"state": "PENDING"},
            {"state": "EXECUTED"},
            {"state": None},
            {"state": "UNKNOWN"},
        ]

        result = analyze_available_statuses(data)

        assert result["EXECUTED"] == 3
        assert result["CANCELED"] == 1
        assert result["PENDING"] == 1
        assert "UNKNOWN" in result


class TestGetStatusInputWithSuggestions:
    """Тесты для функции get_status_input_with_suggestions"""

    @patch("builtins.input", return_value="1")
    def test_numeric_input(self, mock_input: Any) -> None:
        """Тест числового ввода"""
        data = [{"state": "EXECUTED"}, {"state": "CANCELED"}]

        result = get_status_input_with_suggestions(data)
        assert result in ["EXECUTED", "CANCELED"]

    @patch("builtins.input", return_value="EXECUTED")
    def test_text_input(self, mock_input: Any) -> None:
        """Тест текстового ввода"""
        data = [{"state": "EXECUTED"}]

        result = get_status_input_with_suggestions(data)
        assert result == "EXECUTED"


class TestHandleEmptyStatusFilter:
    """Тесты для функции handle_empty_status_filter"""

    @patch("builtins.input", return_value="1")
    def test_exit_choice(self, mock_input: Any) -> None:
        """Тест выбора завершения программы"""
        data = [{"state": "EXECUTED"}]

        result = handle_empty_status_filter(data, "CANCELED")
        assert result["action"] == "exit"
        assert result["transactions"] == []

    @patch("builtins.input", side_effect=["2", "1"])
    @patch("final_modul.get_status_input_with_suggestions", return_value="EXECUTED")
    def test_retry_choice(self, mock_status: Any, mock_input: Any) -> None:
        """Тест выбора повторной попытки"""
        data = [{"state": "EXECUTED", "id": 1}, {"state": "EXECUTED", "id": 2}]

        result = handle_empty_status_filter(data, "CANCELED")
        assert result["action"] == "continue"
        assert len(result["transactions"]) == 2


class TestExtractCategoriesFromTransactions:
    """Тесты для функции extract_categories_from_transactions"""

    def test_empty_data(self):
        """Тест с пустыми данными"""
        assert extract_categories_from_transactions([]) == []

    def test_category_extraction(self):
        """Тест извлечения категорий"""
        data = [
            {"description": "Перевод организации"},
            {"description": "Оплата услуг"},
            {"description": "Перевод организации"},  # Дубликат
            {"description": "Пополнение счета"},
            {"description": ""},  # Пустое описание
            {"description": None},  # None описание
        ]

        result = extract_categories_from_transactions(data)

        assert len(result) == 3
        assert "Перевод организации" in result
        assert "Оплата услуг" in result
        assert "Пополнение счета" in result
        assert "" not in result


# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
