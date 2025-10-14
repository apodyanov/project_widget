"""Главный модуль запуска программы."""

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card
from src.decorators import log
import os
import random
from src.utils import load_transactions
from src.external_api import get_amount_in_rub


if __name__ == "__main__":
    # Вызываем и выводим результат

    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("Счет 64686473678894779589"))
    print(mask_account_card("MasterCard 7158300734726758"))
    print(mask_account_card("Счет 35383033474447895560"))
    print(mask_account_card("Visa Classic 6831982476737658"))
    print(mask_account_card("Visa Platinum 8990922113665229"))
    print(mask_account_card("Visa Gold 5999414228426353"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_date("2024-03-11T02:26:18.671407"))
    # Домашнее задание 10.1 Продвинутый Git
    print(
        filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )
    print(
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )
print('-'*50)
print('Домашнее задание 11.1 Включения и генераторы.')

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]
print('Фильтр по транзакции с валютой: USD')
print(next(filter_by_currency(transactions, "USD")))
print('Вывод описания транзакции')
print(next(transaction_descriptions(transactions)))
print('Генерация номера карты')
print(next(card_number_generator(1234567891234567, 9876543212558979)))
print('-'*50)
print('Домашнее задание 11.2 Декораторы.')


def demonstrate_decorators() -> None:
    """Demonstrate decorators functionality."""
    print("Демонстрация модуля декораторы")
    print("=" * 50)

    # Пример 1: Логирование в консоль
    @log()
    def calculate_sum(a: int, b: int) -> int:
        """Калькуляция суммы двух чисел."""
        return a + b

    @log()
    def divide_numbers(x: float, y: float) -> float:
        """Деление двух чисел."""
        if y == 0:
            raise ValueError("На ноль делить нельзя")
        return x / y

    print("1. Пример записи в консоль:")
    print("-" * 30)

    # Успешное выполнение
    print("Успешное выполнение:")
    result1 = calculate_sum(10, 20)
    print(f"Результат: {result1}")

    # Ошибка
    print("\nВыполнение с ошибкой:")
    try:
        divide_numbers(10, 0)
    except ValueError as e:
        print(f"Обнаружена ошибка: {e}")

    # Пример 2: Логирование в файл
    print("\n2. Пример записи в файл:")
    print("-" * 30)

    @log(filename="demo.log")
    def process_data(data: list, multiplier: int = 2) -> list:
        """Процесс образования списка."""
        return [x * multiplier for x in data]

    @log(filename="demo.log")
    def risky_operation(value: int) -> str:
        """Рисковые значения, которые могут привести к неудаче."""
        if value < 0:
            raise RuntimeError("Отрицательные значения не допускаются")
        return f"Обработка: {value}"

    # Успешное выполнение в файл
    print("Успешное выполнение:")
    result2 = process_data([1, 2, 3, 4, 5])
    print(f"Результат обработки данных: {result2}")

    # Ошибка в файл
    print("\nВыполнение с ошибкой:")
    try:
        risky_operation(-5)
    except RuntimeError as e:
        print(f"Обнаружена ошибка: {e}")

    print("\nПроверьте файл 'demo.log' для детализации")

    # Пример 3: Декоратор с существующими функциями
    print("\n3. Декоратор с существующими функциями:")
    print("-" * 30)

    from src.masks import get_mask_card_number

    # Декорируем существующую функцию
    print("Успешное выполнение:")
    masked_card = log()(get_mask_card_number)

    result3 = masked_card("1234567812345678")
    print(f"Маскировка номера карты: {result3}")

    # Пытаемся декорировать с ошибкой
    print("\nВыполнение с ошибкой:")
    try:
        masked_card("неверный ввод")  # Должно вызвать ошибку
    except ValueError as e:
        print(f"Expected error: {e}")

demonstrate_decorators()

print('-'*50)
print('Домашнее задание 12.1 Библиотеки json, requests и datetime.')
print()
print('='*50)


def main():
    transactions = load_transactions("data/operations.json")
    print(f"Загружено транзакций: {len(transactions)}")
    print("\nСлучайная выборка 5 транзакций:")

    # Случайная выборка 5 транзакций
    if len(transactions) > 5:
        random_transactions = random.sample(transactions, 5)
    else:
        random_transactions = transactions

    # Обрабатываем случайные транзакции
    for i, transaction in enumerate(random_transactions, 1):
        amount_rub = get_amount_in_rub(transaction)

        operation_amount = transaction.get('operationAmount', {})
        original_amount = operation_amount.get('amount', '0')
        currency_code = operation_amount.get('currency', {}).get('code', 'RUB')
        description = transaction.get('description', 'Без описания')

        print(f"\nТранзакция {i}: {description}")
        print(f"  Сумма: {original_amount} {currency_code}")
        print(f"  В рублях: {amount_rub:.2f} RUB")

main()
