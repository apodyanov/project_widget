"""Тесты для модуля widget."""

import pytest
from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    """Тест функции mask_account_card."""

    @pytest.mark.parametrize("input_str, expected", [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1234567812345678", "Maestro 1234 56** **** 5678"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Account 1234567890", "Account **7890"),
        ("Mastercard 5555555555554444", "Mastercard 5555 55** **** 4444"),
    ])
    def test_valid_inputs(self, input_str: str, expected: str) -> None:
        """Тест маскировки различных строк счетов/карт."""
        assert mask_account_card(input_str) == expected

    def test_no_text_before_number(self) -> None:
        """Тест ввода только с цифрой."""
        assert mask_account_card("7000792289606361") == "7000 79** **** 6361"
        assert mask_account_card("73654108430135874305") == "**4305"

    def test_multiple_numbers(self) -> None:
        """Тест ввода нескольких чисел (использует самое длинное)."""
        result = mask_account_card("Card 1234 567812345678 7000792289606361")
        assert "7000 79** **** 6361" in result

    def test_invalid_input(self) -> None:
        """Тест недопустимого ввода."""
        with pytest.raises(ValueError, match="Ввод должен быть непустой строкой"):
            mask_account_card("")

        with pytest.raises(ValueError, match="Ввод должен быть непустой строкой"):
            mask_account_card(None)  # отсутствие ввода

        with pytest.raises(ValueError, match="Нет цифр в веденной строке"):
            mask_account_card("Just text without numbers")

    def test_mixed_content(self) -> None:
        """Тест ввода со смешанным содержанием."""
        result = mask_account_card("Payment to Visa 7000792289606361 for order 12345")
        assert "7000 79** **** 6361" in result
        assert "12345" in result  # не маскировать короткие номера


class TestGetDate:
    """Тест функции get_date."""

    @pytest.mark.parametrize("date_string, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2024-01-01T00:00:00.000000", "01.01.2024"),
        ("2024-02-29T12:30:00.000000", "29.02.2024"),  # високосный год
    ])
    def test_valid_dates(self, date_string: str, expected: str) -> None:
        """Тест форматирования даты с допустимыми входными данными."""
        assert get_date(date_string) == expected

    def test_timezone_handling(self) -> None:
        """Тест дата с часовым поясом."""
        assert get_date("2024-03-11T02:26:18.671407Z") == "11.03.2024"
        assert get_date("2024-03-11T02:26:18.671407+00:00") == "11.03.2024"

    def test_invalid_dates(self) -> None:
        """Тест недопустимых форматов даты."""
        with pytest.raises(ValueError, match="Неверный формат даты"):
            get_date("not-a-date")

        with pytest.raises(ValueError, match="Неверный формат даты"):
            get_date("2024-13-45T99:99:99.999999")  # Invalid date/time

        with pytest.raises(ValueError, match="Ввод должен быть непустой строкой"):
            get_date("")

        with pytest.raises(ValueError, match="Ввод должен быть непустой строкой"):
            get_date(None)  # type: ignore

    def test_edge_cases(self) -> None:
        """Тест граничных случаев для дат."""
        # Минимально действительная дата
        assert get_date("0001-01-01T00:00:00.000000") == "01.01.0001"

        # Различные форматы должны работать.
        assert get_date("2024-03-11T02:26:18") == "11.03.2024"  # Без миллисекунд