from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_currency_via_api, get_amount_in_rub


class TestConvertCurrencyViaApi:
    """Тесты для функции convert_currency_via_api"""

    @patch("src.external_api.requests.get")
    def test_convert_currency_success(self, mock_get):
        """Тест успешной конвертации валюты через API"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": 397.45208,
            "query": {"amount": 5, "from": "USD", "to": "RUB"},
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch.dict("os.environ", {"EXCHANGE_RATE_API_KEY": "test_key"}):
            result = convert_currency_via_api(5.0, "USD", "RUB")
            assert result == 397.45208
            mock_get.assert_called_once()

    @patch("src.external_api.requests.get")
    def test_convert_currency_default_to_rub(self, mock_get):
        """Тест конвертации в рубли по умолчанию"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "result": 950.0}
        mock_get.return_value = mock_response

        with patch.dict("os.environ", {"EXCHANGE_RATE_API_KEY": "test_key"}):
            result = convert_currency_via_api(10.0, "USD")  # Не указываем целевую валюту
            assert result == 950.0

    @patch("src.external_api.requests.get")
    def test_convert_currency_api_error(self, mock_get):
        """Тест обработки ошибки API"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}
        mock_get.return_value = mock_response

        with patch.dict("os.environ", {"EXCHANGE_RATE_API_KEY": "test_key"}):
            with pytest.raises(Exception, match="API error"):
                convert_currency_via_api(100.0, "USD", "RUB")

    @patch("src.external_api.requests.get")
    def test_convert_currency_no_result(self, mock_get):
        """Тест для случая, когда в ответе нет result"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            # Нет поля 'result'
        }
        mock_get.return_value = mock_response

        with patch.dict("os.environ", {"EXCHANGE_RATE_API_KEY": "test_key"}):
            with pytest.raises(Exception, match="Result not found"):
                convert_currency_via_api(100.0, "USD", "RUB")

    def test_no_api_key(self):
        """Тест для случая, когда API ключ не установлен"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="API key not found"):
                convert_currency_via_api(100.0, "USD", "RUB")


class TestGetAmountInRub:
    """Тесты для функции get_amount_in_rub"""

    @patch("src.external_api.convert_currency_via_api")
    def test_api_error_returns_zero(self, mock_convert):
        """Тест, что при ошибке API возвращается 0"""
        mock_convert.side_effect = Exception("API error")

        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        }

        result = get_amount_in_rub(transaction)

        # Проверяем что возвращается 0 при ошибке API
        assert result == 0.0
        # Убеждаемся что API было вызвано
        mock_convert.assert_called_once_with(100.0, "USD", "RUB")

    @patch("src.external_api.convert_currency_via_api")
    def test_rub_transaction_returns_same_amount(self, mock_convert):
        """Тест, что для рублевых транзакций возвращается исходная сумма"""
        transaction = {
            "operationAmount": {
                "amount": "500.0",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            }
        }

        result = get_amount_in_rub(transaction)

        # Для RUB конвертация не должна вызываться
        assert result == 500.0
        mock_convert.assert_not_called()

    @patch("src.external_api.convert_currency_via_api")
    def test_invalid_amount_returns_zero(self, mock_convert):
        """Тест, что при невалидной сумме возвращается 0"""
        transaction = {
            "operationAmount": {
                "amount": "invalid",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        }

        result = get_amount_in_rub(transaction)

        assert result == 0.0
        mock_convert.assert_not_called()

    def test_missing_operation_amount_returns_zero(self):
        """Тест, что при отсутствии operationAmount возвращается 0"""
        transaction = {"id": 1, "state": "EXECUTED"}

        result = get_amount_in_rub(transaction)

        assert result == 0.0

    def test_empty_operation_amount_returns_zero(self):
        """Тест, что при пустом operationAmount возвращается 0"""
        transaction = {"operationAmount": {}}

        result = get_amount_in_rub(transaction)

        assert result == 0.0
