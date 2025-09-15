from typing import Any, Dict, List

"""Функция filter_by_state, которая принимает список словарей и
опционально значение для ключа state (по умолчанию 'EXECUTED').
Функция возвращает новый список словарей, содержащий только те словари,
у которых ключ state соответствует указанному значению."""

"""Пример работы функции:
>>> data = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
            ]
>>> filter_by_state(data)
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
>>> filter_by_state(data, 'CANCELED')
         [{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}]"""


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:

    # Проверка на некорректность типа введенных данных
    if not isinstance(data, list):
        raise TypeError("Тип вводимых данных должен быть 'списком' или 'словарем'")

    if not isinstance(state, str):
        raise TypeError("Тип аргумента 'State' должен быть строкой")

    return [item for item in data if item.get("state") == state]


"""Функция sort_by_date, которая принимает список словарей и необязательный
параметр, задающий порядок сортировки (по умолчанию — убывание).
Функция должна возвращать новый список, отсортированный по дате (date)."""


def sort_by_date(data: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    # Проверка на некорректность типа введенных данных
    if not isinstance(data, list):
        raise TypeError("Тип вводимых данных должен быть 'списком' или 'словарем'")
    # Проверка на отсутствие данных, для ускорения отработки кода
    if not data:
        return []

    # Проверяем что все словари имеют ключ date
    for item in data:
        if "date" not in item:
            raise KeyError("Все словари должны содержать ключ 'date'")

        # Сортируем по дате
    return sorted(data, key=lambda x: x["date"], reverse=descending)
