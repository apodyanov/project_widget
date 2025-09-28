"""Тесты для модуля processing."""

from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тест для функции filter_by_state."""

    @pytest.mark.parametrize(
        "state, expected_count",
        [
            ("EXECUTED", 4),
            ("PENDING", 0),
            ("CANCELED", 1),
            ("COMPLETED", 0),  # Не существующее состояние
        ],
    )
    def test_filter_various_states(
        self, sample_transactions: List[Dict[str, Any]], state: str, expected_count: int
    ) -> None:
        """Тест фильтров по различным состояниям."""
        result = filter_by_state(sample_transactions, state)
        assert len(result) == expected_count
        if expected_count > 0:
            assert all(item["state"] == state for item in result)

    def test_default_state(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтра с состоянием по умолчанию (EXECUTED)."""
        result_default = filter_by_state(sample_transactions)
        result_explicit = filter_by_state(sample_transactions, "EXECUTED")

        assert result_default == result_explicit
        assert len(result_default) == 4
        assert all(item["state"] == "EXECUTED" for item in result_default)

    def test_empty_list(self) -> None:
        """Тест фильтра пустого списка."""
        assert filter_by_state([]) == []
        assert filter_by_state([], "EXECUTED") == []

    def test_no_matching_state(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтра, когда ни один элемент не соответствует состоянию."""
        result = filter_by_state(sample_transactions, "COMPLETED")
        assert result == []

    def test_missing_state_key(self) -> None:
        """Тест фильтра, когда у некоторых элементов отсутствует ключ состояния."""
        data = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
            {"id": 2, "date": "2024-01-02"},  # отсутствует состояние
            {"id": 3, "state": "PENDING", "date": "2024-01-03"},
        ]

        result = filter_by_state(data, "EXECUTED")
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_invalid_input(self) -> None:
        """Тест недопустимого ввода."""
        with pytest.raises(TypeError, match="Тип вводимых данных должен быть 'списком' или 'словарем'"):
            filter_by_state("not a list")  # type: ignore

        with pytest.raises(TypeError, match="Тип аргумента 'State' должен быть строкой"):
            filter_by_state([], 123)  # type: ignore


class TestSortByDate:
    """Тест функции sort_by_date."""

    def test_sort_descending(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест сортировки по убыванию (сначала самые новые)."""
        result = sort_by_date(sample_transactions, descending=True)

        # Проверка на правильность порядка
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, reverse=True)

        #  Проверка особых форматов даты
        assert result[0]["date"] == "2019-04-04T23:20:05.206878"  # Новые
        assert result[-1]["date"] == "2018-06-30T02:08:58.425572"  # Старые

    def test_sort_ascending(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест сортировки по возрастанию (сначала самые старые)."""
        result = sort_by_date(sample_transactions, descending=False)

        # Проверка на правильность порядка
        dates = [item["date"] for item in result]
        assert dates == sorted(dates)

        # Проверка особых форматов даты
        assert result[0]["date"] == "2018-06-30T02:08:58.425572"  # Старые
        assert result[-1]["date"] == "2019-04-04T23:20:05.206878"  # Новые

    def test_default_sort_order(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест, что порядок сортировки по умолчанию — по убыванию."""
        result_default = sort_by_date(sample_transactions)
        result_explicit = sort_by_date(sample_transactions, descending=True)

        assert result_default == result_explicit

    def test_empty_list(self) -> None:
        """Тест на сортировку пустого списка."""
        assert sort_by_date([]) == []
        assert sort_by_date([], descending=False) == []

    def test_single_item(self) -> None:
        """Тест списка сортировки с одним элементом."""
        data = [{"id": 1, "date": "2024-01-01T00:00:00.000000"}]
        result = sort_by_date(data)
        assert result == data

    def test_same_dates(self) -> None:
        """Тест сортировки с одинаковыми датами."""
        data = [
            {"id": 1, "date": "2024-01-01T00:00:00.000000"},
            {"id": 2, "date": "2024-01-01T00:00:00.000000"},
            {"id": 3, "date": "2024-01-01T00:00:00.000000"},
        ]

        result = sort_by_date(data)
        assert len(result) == 3  # Порядок может быть произвольным, но должен сохранять все

    def test_missing_date_key(self) -> None:
        """Тест отсутствующего ключа даты."""
        data = [
            {"id": 1, "date": "2024-01-01T00:00:00.000000"},
            {"id": 2, "state": "EXECUTED"},  # Отсутствует дата
        ]

        with pytest.raises(KeyError, match="Все словари должны содержать ключ 'date'"):
            sort_by_date(data)

    def test_invalid_input(self) -> None:
        """Test handling invalid input."""
        with pytest.raises(TypeError, match="Тип вводимых данных должен быть 'списком' или 'словарем'"):
            sort_by_date("not a list")  # type: ignore
