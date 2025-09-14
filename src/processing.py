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

from typing import List, Dict, Any, Optional


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    # Проверка на некорректность типа введенных данных
    if not isinstance(data, list):
        raise TypeError("Data must be a list of dictionaries")

    if not isinstance(state, str):
        raise TypeError("State must be a string")

    return [item for item in data if item.get("state") == state]

result = filter_by_state([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
            ])
print(result)