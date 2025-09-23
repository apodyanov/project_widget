"""Тесты для модуля masks, структурированы в классы, для лучшей читаемости кода."""

import pytest

from src.masks import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:
    """Тест функции get_mask_card_number."""

    @pytest.mark.parametrize(
        "card_number, expected",
        [
            ("7000792289606361", "7000 79** **** 6361"),
            ("1234567812345678", "1234 56** **** 5678"),
            ("4111111111111111", "4111 11** **** 1111"),
            ("5555555555554444", "5555 55** **** 4444"),
        ],
    )
    def test_valid_card_numbers(self, card_number: str, expected: str) -> None:
        """Тест маскировки правильных номеров карт."""
        assert get_mask_card_number(card_number) == expected

    def test_invalid_card_length(self) -> None:
        """Тест недопустимой длины номера карты."""
        with pytest.raises(ValueError, match="Номер карты должен быть только из 16 цифр"):
            get_mask_card_number("1234567890")  # Короткий номер

        with pytest.raises(ValueError, match="Номер карты должен быть только из 16 цифр"):
            get_mask_card_number("12345678123456781234")  # Длинный номер

    def test_non_digit_characters(self) -> None:
        """Тест недопустимости содержания в номере не цифр."""
        with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
            get_mask_card_number("700079228960636a")  # Содержит букву

        with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
            get_mask_card_number("7000-7922-8960-6361")  # Содержит дефисы

    def test_empty_string(self) -> None:
        """Тест не допустимости пустой строки."""
        with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
            get_mask_card_number("")

    @pytest.mark.parametrize(
        "card_number",
        [
            "0000000000000000",  # Все ноли
            "9999999999999999",  # Все девятки
            "1234123412341234",  # Шаблоны
        ],
    )
    def test_edge_cases(self, card_number: str) -> None:
        """Тестирование крайних случаев для номеров карт."""
        result = get_mask_card_number(card_number)
        assert len(result) == 19  # 4+4+4+4+3
        assert "**" in result
        assert result.startswith(card_number[:4])
        assert result.endswith(card_number[-4:])


class TestGetMaskAccount:
    """Тест функции get_mask_account."""

    @pytest.mark.parametrize(
        "account_number, expected",
        [
            ("73654108430135874305", "**4305"),
            ("12345678901234567890", "**7890"),
            ("40817810099910004312", "**4312"),
            ("9876543210", "**3210"),
        ],
    )
    def test_valid_account_numbers(self, account_number: str, expected: str) -> None:
        """Тест маскировки действительных номеров счетов."""
        assert get_mask_account(account_number) == expected

    def test_short_account_number(self) -> None:
        """Тест коротких номеров счетов."""
        with pytest.raises(ValueError, match="Номер счета должен содержать минимум 4 цифры"):
            get_mask_account("123")  # Короткий номер

        # Exactly 4 digits should work
        assert get_mask_account("1234") == "**1234"

    def test_non_digit_characters(self) -> None:
        """Тест нецифровых символов."""
        with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
            get_mask_account("7365410843013587430a")  # Contains letter

        with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
            get_mask_account("40817 8100999 10004312")  # Contains spaces

    def test_empty_string(self) -> None:
        """Тест на пустую строку."""
        with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
            get_mask_account("")

    @pytest.mark.parametrize(
        "account_number",
        [
            "00000000000000000000",  # Все ноли
            "99999999999999999999",  # Все девятки
            "1234567890",  # 10 цифр
            "12345678901234567890",  # 20 цифр
        ],
    )
    def test_edge_cases(self, account_number: str) -> None:
        """Тест пограничных случаев для номеров счетов."""
        result = get_mask_account(account_number)
        assert result.startswith("**")
        assert result.endswith(account_number[-4:])
        assert len(result) == 6  # ** + 4 цифры
