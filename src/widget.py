"""Модуль с функцией mask_account_card, которая обрабатывает информацию
как о картах, так и о счетах.
Функция принимает один аргумент — строку, содержащую тип и номер карты или счета.
Аргументом может быть строка типа
Visa Platinum 7000792289606361, или Счет 73654108430135874305,
разделять строку на 2 аргумента - отдельно имя, отдельно номер, нельзя!
Функция возвращает строку с замаскированным номером. Для карт и счетов использует
разные типы маскировки.

Ошибки при вводе данных Raises:
ValueError: Если во входной строке не найдено число

Примеры работы функции
Пример для карты
Visa Platinum 7000792289606361 # входной аргумент
Visa Platinum 7000 79** **** 6361 # выход функции

Пример для счета
Счет 73654108430135874305 # входной аргумент
Счет **4305 # выход функции"""

import re
from datetime import datetime


from .masks import get_mask_card_number, get_mask_account


def mask_account_card(account_info: str) -> str:

    # Проверка на ввод пустой строки
    if not account_info or not isinstance(account_info, str):
        raise ValueError("Ввод должен быть непустой строкой")

        # Проверка на наличие цифр в веденной строке
    numbers = re.findall(r'\d+', account_info)
    if not numbers:
        raise ValueError("Нет цифр в веденной строке")

        # Берем самый длинный номер (основной)
    number_str = str(max(numbers, key=len))
    lower_info = account_info.lower()

    # Определяем тип введённых данных - "карта" или "счет"
    is_card = ((any(word in lower_info for word in
                ["visa", "mastercard", "maestro",
                 "visa classic", "card", "visa platinum", "visa gold"])
                    or len(number_str) == 16)
                    and not any(word in lower_info for word in ["счет"]))

    # Выбираем функцию маскировки и применяем
    if is_card:
        masked_number = get_mask_card_number(number_str)
    else:
        masked_number = get_mask_account(number_str)

    return account_info.replace(number_str, masked_number)


def get_date(date_string: str) -> str:
    """ Функция, которая принимает на вход строку с датой в формате:
"2024-03-11T02:26:18.671407" и возвращает строку с датой в формате:
"ДД.ММ.ГГГГ" ("11.03.2024").

    Raises:
        ValueError: Если ввод строки не соответствует формату
    """
    if not date_string or not isinstance(date_string, str):
        raise ValueError("Ввод должен быть непустой строкой")

    try:
        # Парсинг ISO формат
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        # Форматируем в DD.MM.YYYY
        return dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid date format: {date_string}") from e
