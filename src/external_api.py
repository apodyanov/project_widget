import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


def convert_currency_via_api(amount: float, from_currency: str, to_currency: str = 'RUB') -> float:
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
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please set EXCHANGE_RATE_API_KEY in .env file")

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"
    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get('success', False):
            error_info = data.get('error', {}).get('info', 'Unknown error')
            raise Exception(f"API error: {error_info}")

        # Возвращаем готовую конвертированную сумму из ответа
        result = data.get('result')
        if result is None:
            raise Exception("Result not found in API response")

        return result

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
    except KeyError as e:
        raise Exception(f"Invalid response format: {str(e)}")


def get_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Принимает на вход транзакцию и возвращает сумму транзакции в рублях.

    Args:
        transaction (Dict[str, Any]): Словарь с данными о транзакции

    Returns:
        float: Сумма транзакции в рублях
    """
    try:
        # Извлекаем данные из вложенной структуры
        operation_amount = transaction.get('operationAmount', {})
        amount_str = operation_amount.get('amount', '0')
        currency_info = operation_amount.get('currency', {})
        currency_code = currency_info.get('code', 'RUB')

        # Преобразуем сумму в float
        amount = float(amount_str)

        # Если валюта уже рубли, возвращаем как есть
        if currency_code == 'RUB':
            return amount

        # Если валюта USD или EUR, конвертируем через API endpoint /convert
        if currency_code in ['USD', 'EUR']:
            converted_amount = convert_currency_via_api(amount, currency_code, 'RUB')
            return converted_amount

        # Для других валют возвращаем как есть (не конвертируем)
        return amount

    except (ValueError, TypeError):
        # Если не удалось преобразовать сумму в число
        return 0.0
    except Exception:
        # Если произошла ошибка при конвертации через API
        return 0.0
