"""Модуль с финальными функциями используемыми в главном модуле программы"""

import re
from collections import Counter
from typing import Any
from typing import Counter as CounterType
from typing import Dict, List

from src import get_mask_account, get_mask_card_number


class SearchError(Exception):
    """Пользовательское исключение для ошибок поиска"""

    pass


class CategoryProcessingError(Exception):
    """Пользовательское исключение для ошибок обработки категорий"""

    pass


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Поиск строки во всех полях банковских операций.

    Args:
        data: Список словарей с транзакциями
        search: Строка для поиска

    Returns:
        List[Dict]: Отфильтрованный список транзакций
    """
    if not data or not search:
        return []

    filtered_data = []

    try:
        pattern = re.compile(re.escape(search), re.IGNORECASE)

        for transaction in data:
            # Проверяем все значения в словаре транзакции
            for value in transaction.values():
                if value and pattern.search(str(value)):
                    filtered_data.append(transaction)
                    break

    except SearchError as e:
        print(f"Ошибка при обработке данных: {e}")
        return []

    return filtered_data


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Принимает список словарей с данными о банковских операциях и список категорий операций,
    возвращает словарь, в котором ключи - это названия категорий, а значения -
    количество операций в каждой категории.

    Категории операций хранятся в поле description.

    Args:
        data: Список словарей с транзакциями
        categories: Список категорий для подсчета

    Returns:
        Dict[str, int]: Словарь {категория: количество_операций}
    """
    if not data or not categories:
        return {}

    try:
        # Создаем набор категорий для быстрого поиска (без учета регистра)
        categories_lower = {cat.lower() for cat in categories}

        # Используем Counter для подсчета
        category_counter: CounterType[str] = Counter()

        for transaction in data:
            description = transaction.get("description", "")

            if not description:
                continue

            description_lower = str(description).lower()

            # Проверяем каждую категорию на вхождение в описании
            for category in categories_lower:
                if category in description_lower:
                    # Сохраняем оригинальное название категории
                    original_category = next(cat for cat in categories if cat.lower() == category)
                    category_counter[original_category] += 1

        return dict(category_counter)

    except CategoryProcessingError as e:
        raise ValueError(f"Ошибка при обработке данных: {e}")


def format_account_display(account_info: str) -> str:
    """
    Форматирует отображение счета или карты с маскировкой

    Args:
        account_info: Информация о счете/карте

    Returns:
        str: Отформатированная строка
    """
    if not account_info:
        return "Не указано"

    # Определяем тип: карта или счет
    if "счет" in account_info.lower():
        parts = account_info.split()
        if len(parts) > 1:
            account_number = parts[-1]
            masked_account = get_mask_account(account_number)
            return f"Счет {masked_account}"
        return account_info
    else:
        # Это карта - извлекаем номер карты (последняя последовательность цифр)
        parts = account_info.split()
        for part in reversed(parts):
            if part.isdigit() and len(part) == 16:
                masked_card = get_mask_card_number(part)
                # Сохраняем название карты
                card_name = " ".join(parts[:-1]) if len(parts) > 1 else "Карта"
                return f"{card_name} {masked_card}"
        return account_info


def format_transaction_display(transaction: Dict[str, Any]) -> str:
    """
    Форматирует транзакцию для красивого вывода

    Args:
        transaction: Данные транзакции

    Returns:
        str: Отформатированная строка
    """
    # Извлекаем данные с альтернативными названиями полей
    date = str(transaction.get("date", transaction.get("Date", "")))[:10]
    description = str(transaction.get("description", transaction.get("Description", "Без описания")))
    from_account = str(transaction.get("from", transaction.get("From", "")))
    to_account = str(transaction.get("to", transaction.get("To", "")))

    # Универсальное извлечение информации о сумме и валюте
    operation_amount = transaction.get("operationAmount", {})

    # Определяем сумму и валюту в зависимости от формата данных
    if isinstance(operation_amount, dict):
        # JSON формат
        amount_data = {
            "amount": str(operation_amount.get("amount", "0")),
            "currency_code": str(operation_amount.get("currency", {}).get("code", "RUB")),
            "currency_name": str(operation_amount.get("currency", {}).get("name", "")),
        }
    else:
        # CSV/XLSX формат
        amount_data = {
            "amount": str(transaction.get("amount", transaction.get("Amount", "0"))),
            "currency_code": str(transaction.get("currency_code", transaction.get("Currency", "RUB"))),
            "currency_name": str(transaction.get("currency_name", transaction.get("CurrencyName", ""))),
        }

    # Очищаем и нормализуем значения
    amount = amount_data["amount"] if amount_data["amount"] != "None" else "0"
    currency_code = amount_data["currency_code"] if amount_data["currency_code"] != "None" else "RUB"
    currency_name = amount_data["currency_name"] if amount_data["currency_name"] != "None" else "руб."

    # Если валюта не указана, предполагаем RUB
    if not currency_code:
        currency_code = "RUB"
        currency_name = "руб." if not currency_name else currency_name

    # Форматируем вывод как dictionary literal для построения строки
    result_parts = {"header": f"{date} {description}\n", "accounts": "", "amount": f"Сумма: {amount} {currency_code}"}

    # Добавляем информацию о счетах
    if from_account and from_account != "None" and from_account != "":
        result_parts["accounts"] += f"{format_account_display(from_account)} -> "

    if to_account and to_account != "None" and to_account != "":
        result_parts["accounts"] += f"{format_account_display(to_account)}\n"
    else:
        result_parts["accounts"] += "\n"

    # Добавляем название валюты если оно отличается от кода
    if currency_name and currency_name != currency_code:
        result_parts["amount"] += f" ({currency_name})"

    result_parts["amount"] += "\n"

    # Собираем финальную строку
    return result_parts["header"] + result_parts["accounts"] + result_parts["amount"]


def get_user_choice(prompt: str, valid_choices: List[str]) -> str:
    """
    Получает выбор пользователя с валидацией

    Args:
        prompt: Текст запроса
        valid_choices: Список допустимых ответов

    Returns:
        str: Выбор пользователя
    """
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(f"Некорректный ввод. Допустимые варианты: {', '.join(valid_choices)}")


def sort_by_date(data: List[Dict], reverse: bool = False) -> List[Dict]:
    """
    Сортирует транзакции по дате
    """
    if not data:
        return []

    valid_transactions = []
    for transaction in data:
        date = transaction.get("date", "")
        if date and date != "None":
            valid_transactions.append(transaction)

    return sorted(valid_transactions, key=lambda x: x.get("date", ""), reverse=reverse)


def filter_rub_transactions(data: List[Dict]) -> List[Dict]:
    """
    Фильтрует только рублевые транзакции

    Args:
        data: Список транзакций

    Returns:
        List[Dict]: Только рублевые транзакции
    """
    if not data:
        return []

    rub_transactions = []
    for transaction in data:
        operation_amount = transaction.get("operationAmount")
        currency_code = ""

        # Проверяем, что operation_amount - это словарь
        if isinstance(operation_amount, dict):
            currency_info = operation_amount.get("currency")

            # Проверяем, что currency_info - это словарь
            if isinstance(currency_info, dict):
                currency_code = str(currency_info.get("code", ""))

        if currency_code == "RUB":
            rub_transactions.append(transaction)

    return rub_transactions


def get_search_suggestions(transactions: List[Dict]) -> List[str]:
    """
    Возвращает список популярных слов из описаний транзакций для подсказок пользователю
    """
    # Собираем все слова из описаний
    all_words = []
    for transaction in transactions:
        description = str(transaction.get("description", ""))
        # Разбиваем на слова, убираем специальные символы, приводим к нижнему регистру
        words = re.findall(r"\b[а-яa-z]{3,}\b", description.lower())
        all_words.extend(words)

    # Считаем частоту слов
    word_freq = Counter(all_words)

    # Исключаем служебные слова (русские и английские)
    common_words = {
        "и",
        "в",
        "на",
        "с",
        "по",
        "для",
        "из",
        "от",
        "до",
        "не",
        "у",
        "за",
        "к",
        "о",
        "об",
        "the",
        "and",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
    }

    # Берем топ-7 самых частых слов (длиной больше 2 символов и не служебные)
    suggestions = [word for word, count in word_freq.most_common(15) if len(word) > 2 and word not in common_words][:7]

    return suggestions


def analyze_available_statuses(transactions: List[Dict]) -> Dict[str, int]:
    """
    Анализирует доступные статусы в данных и возвращает статистику
    """
    available_stats: Dict[str, int] = {}

    for transaction in transactions:
        state_value = transaction.get("state")
        if state_value is not None:
            state_str = str(state_value).upper()
            available_stats[state_str] = available_stats.get(state_str, 0) + 1

    return available_stats


def get_status_input_with_suggestions(transactions: List[Dict[str, Any]]) -> str:
    """
    Получает статус операции от пользователя с подсказками о доступных статусах
    """
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}

    # Получаем уникальные статусы из транзакций, но только валидные
    existing_statuses: set[str] = set()
    for transaction in transactions:
        status = transaction.get("state", "").upper()
        if status in valid_statuses:
            existing_statuses.add(status)

    # Преобразуем в список и сортируем для удобства
    existing_statuses_list: List[str] = sorted(list(existing_statuses))

    print("\nДоступные статусы операций в выбранном файле:")
    for i, status in enumerate(existing_statuses_list, 1):
        print(f"{i}. {status}")

    while True:
        try:
            choice = input("\nВведите номер статуса или название статуса: ").strip().upper()

            # Если ввели номер
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(existing_statuses):
                    return existing_statuses_list[choice_num - 1]
                else:
                    print(f"Пожалуйста, введите число от 1 до {len(existing_statuses_list)}")

            # Если ввели текст
            else:
                if choice in valid_statuses:
                    # Проверяем, есть ли такой статус в данных
                    if choice in existing_statuses:
                        return choice
                    else:
                        print(f"Статус '{choice}' допустим, но не найден в текущих данных.")
                        print("Выберите один из доступных статусов:")
                        for i, status in enumerate(existing_statuses_list, 1):
                            print(f"{i}. {status}")
                else:
                    print("Недопустимый статус. Допустимые статусы: EXECUTED, CANCELED, PENDING")
                    print("Доступные статусы в данном файле:")
                    for i, status in enumerate(existing_statuses_list, 1):
                        print(f"{i}. {status}")

        except (ValueError, IndexError):
            print("Пожалуйста, введите корректный номер или название статуса")


def handle_empty_status_filter(transactions: List[Dict[str, Any]], status: str) -> Dict[str, Any]:
    """
    Обрабатывает ситуацию, когда после фильтрации по статусу не найдено транзакций.
    Возвращает словарь с решением пользователя и отфильтрованными транзакциями
    """
    while True:
        print(f'\nНе найдено транзакций со статусом "{status}"')
        print("Выберите действие:")
        print("1. Завершить программу")
        print("2. Выбрать другой статус для данного файла")

        choice = get_user_choice("Ваш выбор (1 или 2): ", ["1", "2"])

        if choice == "1":
            return {"action": "exit", "transactions": []}
        else:
            # Выбираем другой статус
            new_status = get_status_input_with_suggestions(transactions)
            new_filtered_transactions = process_bank_search(transactions, new_status)

            if new_filtered_transactions:
                print(f'Операции отфильтрованы по статусу "{new_status}"')
                print(f"Найдено операций: {len(new_filtered_transactions)}")
                return {"action": "continue", "transactions": new_filtered_transactions}
            else:
                # Рекурсивно вызываем эту же функцию для нового статуса
                return handle_empty_status_filter(transactions, new_status)


def extract_categories_from_transactions(transactions: List[Dict[str, Any]]) -> List[str]:
    """
    Извлекает уникальные описания транзакций как категории
    """
    categories: set[str] = set()

    for transaction in transactions:
        description = transaction.get("description", "")
        if description:
            # Берем описание целиком как категорию
            categories.add(str(description).strip())

    return sorted(list(categories))
