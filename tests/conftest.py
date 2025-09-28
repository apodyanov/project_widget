"""Фикстуры для тестов."""

from datetime import datetime
from typing import Any, Dict, List

import pytest


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
        {"Maestro": "1234567812345678"},
        {"Счет": "73654108430135874305"},
        {"Account": "1234567890"},
        {"Mastercard": "5555555555554444"},
        {"Счет": "40817810099910004312"}
    ]


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с образцами транзакций для тестирования."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "рублей",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "рублей",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]


@pytest.fixture
def mixed_currency_transactions() -> List[Dict[str, Any]]:
    """Фикстура со смешанными валютными операциями."""
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            },
            "description": "USD Transaction"
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "200.00",
                "currency": {"code": "EUR"}
            },
            "description": "EUR Transaction"
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "300.00",
                "currency": {"code": "USD"}
            },
            "description": "Another USD Transaction"
        },
        {
            "id": 4,
            "operationAmount": {
                "amount": "400.00",
                "currency": {"code": "GBP"}
            },
            "description": "GBP Transaction"
        }
    ]


@pytest.fixture
def transactions_with_missing_fields() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями в которых отсутствуют некоторые поля."""
    return [
        {
            "id": 1,
            "description": "Complete transaction",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        },
        {
            "id": 2,
            "description": "Missing operationAmount"
            # Нет operationAmount
        },
        {
            "id": 3,
            "description": "Missing currency",
            "operationAmount": {
                "amount": "300.00"
                # Нет currency
            }
        },
        {
            "id": 4,
            "description": "Missing description",
            "operationAmount": {
                "amount": "400.00",
                "currency": {"code": "EUR"}
            }
        },
        {
            "id": 5,
            # Нет description
            "operationAmount": {
                "amount": "500.00",
                "currency": {"code": "USD"}
            }
        }
    ]