"""Фикстуры для тестов."""

import pytest
from datetime import datetime
from typing import Dict, List, Any


@pytest.fixture
def sample_card_numbers() -> List[str]:
    """Фикстура с различными номерами карт для тестирования."""
    return [
        "7000792289606361",  # 16 цифр
        "1234567812345678",  # 16 цифр
        "4111111111111111",  # Visa test
        "5555555555554444",  # Mastercard test
    ]


@pytest.fixture
def sample_account_numbers() -> List[str]:
    """Фикстура с различными номерами счета для тестирования."""
    return [
        "73654108430135874305",  # 20 цифр
        "12345678901234567890",  # 20 цифр
        "40817810099910004312",  # Реалистичный счет
        "9876543210",  # 10 цифр
    ]


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с образцами транзакций для тестирования."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:30:00.000000", "amount": "100.50"},
        {"id": 2, "state": "PENDING", "date": "2024-01-10T14:25:00.000000", "amount": "200.00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-20T09:15:00.000000", "amount": "300.75"},
        {"id": 4, "state": "CANCELED", "date": "2024-01-05T16:45:00.000000", "amount": "400.25"},
        {"id": 5, "state": "EXECUTED", "date": "2024-01-25T11:20:00.000000", "amount": "500.00"},
    ]


@pytest.fixture
def sample_dates() -> List[str]:
    """Фикстура с различными форматами даты для тестирования."""
    return [
        "2024-03-11T02:26:18.671407",
        "2023-12-31T23:59:59.999999",
        "2024-01-01T00:00:00.000000",
        "2024-02-29T12:30:00.000000",  # Високосный год
    ]


@pytest.fixture
def mixed_account_data() -> List[Dict[str, Any]]:
    """Фикстура со смешанными данными счета/карты для тестирования виджета."""
    return [
        {"Visa Platinum": "7000792289606361"},
        "Maestro 1234567812345678",
        "Счет 73654108430135874305",
        "Account 1234567890",
        "Mastercard 5555555555554444",
        "Счет 40817810099910004312",
    ]
