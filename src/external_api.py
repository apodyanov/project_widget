import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class CurrencyConversionError(Exception):
    """Пользовательское исключение для ошибок конвертации валют"""

    pass


class APIError(Exception):
    """Пользовательское исключение для ошибок API"""

    pass


def convert_currency_via_api(amount: float, from_currency: str, to_currency: str = "RUB") -> Any:
    """
    Конвертирует сумму из одной валюты в другую используя внешнее API endpoint /convert.

    Args:
        amount (float): Сумма для конвертации
        from_currency (str): Исходная валюта (USD, EUR)
        to_currency (str): Целевая валюта (по умолчанию RUB)

    Returns:
        float: Конвертированная сумма в рублях

    Raises:
        Exception: Если произошла ошибка при запросе к API
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set EXCHANGE_RATE_API_KEY in .env file")

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"
    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get("success", False):
            error_info = data.get("error", {}).get("info", "Unknown error")
            raise APIError(f"API error: {error_info}")

        # Возвращаем готовую конвертированную сумму из ответа
        result = data.get("result")
        if result is None:
            raise APIError("Result not found in API response")

        return result

    except requests.exceptions.RequestException as e:
        raise CurrencyConversionError(f"Request failed: {str(e)}")
    except KeyError as e:
        raise CurrencyConversionError(f"Invalid response format: {str(e)}")


def get_amount_in_rub(transaction: Dict[str, Any]) -> Any:
    """
    Принимает на вход транзакцию и возвращает сумму транзакции в рублях.

    Args:
        transaction (Dict[str, Any]): Словарь с данными о транзакции

    Returns:
        float: Сумма транзакции в рублях
    """
    try:
        # Извлекаем информацию о сумме и валюте
        operation_amount = transaction.get('operationAmount', {})

        if not operation_amount:
            return 0.0

        amount_str = operation_amount.get('amount', '0')
        currency_info = operation_amount.get('currency', {})
        currency_code = currency_info.get('code', 'RUB')

        # Пытаемся преобразовать сумму в число
        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            return 0.0

        # Если уже рубли, возвращаем как есть
        if currency_code == 'RUB':
            return amount

        # Конвертируем через API
        converted_amount = convert_currency_via_api(amount, currency_code, "RUB")
        return converted_amount

    except Exception:
        # В случае любой ошибки возвращаем 0
        return 0.0
