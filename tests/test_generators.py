"""Тесты модуля генераторов."""

import pytest
from typing import List, Dict, Any
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


class TestFilterByCurrency:
    """Тест функции-генератора filter_by_currency."""

    def test_filter_usd_transactions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтра USD транзакций."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))

        assert len(usd_transactions) == 3
        assert all(
            transaction["operationAmount"]["currency"]["code"] == "USD"
            for transaction in usd_transactions
        )
        # Проверяем конкретные ID USD транзакций
        usd_ids = {transaction["id"] for transaction in usd_transactions}
        expected_ids = {939719570, 142264268, 895315941}
        assert usd_ids == expected_ids

    def test_filter_rub_transactions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтра RUB транзакций."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))

        assert len(rub_transactions) == 2
        assert all(
            transaction["operationAmount"]["currency"]["code"] == "RUB"
            for transaction in rub_transactions
        )

    def test_filter_nonexistent_currency(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтра для валюты, которой не существует."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        assert len(eur_transactions) == 0

    def test_empty_transactions_list(self) -> None:
        """Тест фильтра пустого списка транзакций."""
        transactions = list(filter_by_currency([], "USD"))
        assert transactions == []

    def test_generator_behavior(self, mixed_currency_transactions: List[Dict[str, Any]]) -> None:
        """Тест, что функция возвращает генератор и выдает корректные результаты."""
        generator = filter_by_currency(mixed_currency_transactions, "USD")

        # Проверяем что это генератор
        assert hasattr(generator, '__iter__')
        assert hasattr(generator, '__next__')

        # Проверяем поочередное получение элементов
        first = next(generator)
        assert first["id"] == 1

        second = next(generator)
        assert second["id"] == 3

        # Должен вызвать StopIteration
        with pytest.raises(StopIteration):
            next(generator)

    def test_transactions_with_missing_fields(self, transactions_with_missing_fields: List[Dict[str, Any]]) -> None:
        """Тест фильтра транзакций с отсутствующими полями."""
        usd_transactions = list(filter_by_currency(transactions_with_missing_fields, "USD"))

        # Должны найти только транзакции с полной структурой и USD валютой
        assert len(usd_transactions) == 2
        usd_ids = {transaction["id"] for transaction in usd_transactions}
        assert usd_ids == {1, 5}

    @pytest.mark.parametrize("currency_code, expected_count", [
        ("USD", 3),
        ("RUB", 2),
        ("EUR", 0),
        ("GBP", 0),
    ])
    def test_multiple_currencies_parametrized(
            self,
            sample_transactions: List[Dict[str, Any]],
            currency_code: str,
            expected_count: int
    ) -> None:
        """Параметризация теста для нескольких кодов валют."""
        transactions = list(filter_by_currency(sample_transactions, currency_code))
        assert len(transactions) == expected_count


class TestTransactionDescriptions:
    """Тест функции-генератора transaction_descriptions."""

    def test_extract_descriptions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест на извлечение описаний из транзакций."""
        descriptions = list(transaction_descriptions(sample_transactions))

        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации"
        ]

        assert descriptions == expected_descriptions
        assert len(descriptions) == 5

    def test_empty_transactions_list(self) -> None:
        """Тест на извлечение описаний из пустого списка."""
        descriptions = list(transaction_descriptions([]))
        assert descriptions == []

    def test_generator_behavior(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест, что функция возвращает генератор и выдает описания."""
        generator = transaction_descriptions(sample_transactions)

        # Проверяем что это генератор
        assert hasattr(generator, '__iter__')
        assert hasattr(generator, '__next__')

        # Проверяем поочередное получение описаний
        assert next(generator) == "Перевод организации"
        assert next(generator) == "Перевод со счета на счет"

    def test_transactions_with_missing_descriptions(self,
                                                    transactions_with_missing_fields: List[Dict[str, Any]]) -> None:
        """Тест на извлечение описаний из транзакций с отсутствующими полями."""
        descriptions = list(transaction_descriptions(transactions_with_missing_fields))

        # Должны получить только транзакции с описанием
        expected_descriptions = [
            "Complete transaction",
            "Missing operationAmount",
            "Missing currency",
            "Missing description"
        ]

        assert descriptions == expected_descriptions
        assert len(descriptions) == 4


class TestCardNumberGenerator:
    """Тест функции-генератора card_number_generator."""

    @pytest.mark.parametrize("start, end, expected_output", [
        (1, 3, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003"
        ]),
        (9999999999999998, 9999999999999999, [
            "9999 9999 9999 9998",
            "9999 9999 9999 9999"
        ]),
        (1234567812345678, 1234567812345678, [
            "1234 5678 1234 5678"
        ]),
    ])
    def test_valid_ranges(self, start: int, end: int, expected_output: List[str]) -> None:
        """Тест функции-генератора с допустимыми диапазонами чисел."""
        result = list(card_number_generator(start, end))
        assert result == expected_output

    def test_single_number(self) -> None:
        """Тест генерации единичного номера карты."""
        result = list(card_number_generator(42, 42))
        assert result == ["0000 0000 0000 0042"]

    def test_format_correctness(self) -> None:
        """Тест на правильность форматирования номеров карт."""
        numbers = list(card_number_generator(1, 5))

        for number in numbers:
            # Проверяем формат: XXXX XXXX XXXX XXXX
            assert len(number) == 19  # 16 цифр + 3 пробела
            parts = number.split(" ")
            assert len(parts) == 4
            assert all(len(part) == 4 for part in parts)
            assert all(part.isdigit() for part in parts)

    def test_generator_behavior(self) -> None:
        """Тест, что функция генератор."""
        generator = card_number_generator(1, 5)

        # Проверяем что это генератор
        assert hasattr(generator, '__iter__')
        assert hasattr(generator, '__next__')

        # Проверяем поочередное получение номеров
        assert next(generator) == "0000 0000 0000 0001"
        assert next(generator) == "0000 0000 0000 0002"

    def test_invalid_range_too_low(self) -> None:
        """Тест со слишком низким начальным значением."""
        with pytest.raises(ValueError, match="Номер карты должен быть 0000000000000001 and 9999999999999999"):
            list(card_number_generator(0, 5))

    def test_invalid_range_too_high(self) -> None:
        """Тест со слишком высоким конечным значением."""
        with pytest.raises(ValueError, match="Номер карты должен быть 0000000000000001 and 9999999999999999"):
            list(card_number_generator(1, 10000000000000000))

    def test_invalid_range_start_gt_end(self) -> None:
        """Тест с началом больше конца."""
        with pytest.raises(ValueError, match="Start должен быть меньше или эквивалентен end"):
            list(card_number_generator(10, 5))

    @pytest.mark.parametrize("number, expected_format", [
        (1, "0000 0000 0000 0001"),
        (1234, "0000 0000 0000 1234"),
        (12345678, "0000 0000 1234 5678"),
        (1234567812345678, "1234 5678 1234 5678"),
    ])
    def test_specific_number_formats(self, number: int, expected_format: str) -> None:
        """Тест на форматирование конкретных чисел."""
        result = list(card_number_generator(number, number))
        assert result[0] == expected_format