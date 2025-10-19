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

    def test_rub_transaction(self):
        """Тест для транзакции в рублях"""
        transaction = {"operationAmount": {"amount": "1000.50", "currency": {"name": "руб.", "code": "RUB"}}}

        result = get_amount_in_rub(transaction)
        assert result == 1000.50
        assert isinstance(result, float)

    @patch("src.external_api.convert_currency_via_api")
    def test_usd_transaction(self, mock_convert):
        """Тест для транзакции в USD"""
        mock_convert.return_value = 9550.0

        transaction = {"operationAmount": {"amount": "100.0", "currency": {"name": "USD", "code": "USD"}}}

        result = get_amount_in_rub(transaction)
        assert result == 9550.0
        mock_convert.assert_called_once_with(100.0, "USD", "RUB")

    @patch("src.external_api.convert_currency_via_api")
    def test_eur_transaction(self, mock_convert):
        """Тест для транзакции в EUR"""
        mock_convert.return_value = 10500.0

        transaction = {"operationAmount": {"amount": "100.0", "currency": {"name": "EUR", "code": "EUR"}}}

        result = get_amount_in_rub(transaction)
        assert result == 10500.0
        mock_convert.assert_called_once_with(100.0, "EUR", "RUB")

    def test_unknown_currency(self):
        """Тест для транзакции с неизвестной валютой"""
        transaction = {"operationAmount": {"amount": "100.0", "currency": {"name": "GBP", "code": "GBP"}}}

        result = get_amount_in_rub(transaction)
        assert result == 100.0

    @patch("src.external_api.convert_currency_via_api")
    def test_api_error_returns_zero(self, mock_convert):
        """Тест, что при ошибке API возвращается 0"""
        mock_convert.side_effect = Exception("API error")

        transaction = {"operationAmount": {"amount": "100.0", "currency": {"name": "USD", "code": "USD"}}}

        result = get_amount_in_rub(transaction)
        assert result == 0.0
