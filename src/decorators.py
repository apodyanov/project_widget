"""Модуль для декораторов, включающий функцию логирования."""

import functools
from datetime import datetime
from typing import Any, Callable, Optional, TypeVar, cast

# Типовые переменные для более точной типизации
F = TypeVar("F", bound=Callable[..., Any])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """Декоратор, который логирует детали выполнения функции.

    Args:
        filename: Опционально, если имя указано, запись в фай. Если не указано, запись в консоль.

    Returns:
        Декорируемая функция с логированием функционала.

    Examples:
        # >>> @log()
        # ... def add(a: int, b: int) -> int:
        # ...     return a + b
        #
        # >>> @log(filename="app.log")
        # ... def divide(a: int, b: int) -> float:
        # ...     return a / b
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Подготовка информации о функции.
            func_name = func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # Выполнение функции
                result = func(*args, **kwargs)

                # Логирование
                log_message = f"{timestamp} - {func_name} ok\n"
                _write_log(log_message, filename)

                return result

            except Exception as e:
                # Логирование ошибки с детализацией
                error_type = type(e).__name__
                args_str = ", ".join(repr(arg) for arg in args)
                kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
                inputs = f"({args_str})"
                if kwargs_str:
                    inputs += f", {{{kwargs_str}}}"

                log_message = f"{timestamp} - {func_name} error: {error_type}. Inputs: {inputs}\n"
                _write_log(log_message, filename)

                # Повторный вызов исключения
                raise

        return cast(F, wrapper)

    return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """Запись лога в файл или в консоль.

    Args:
        message: Сообщение лога для записи
        filename: Опционально, имя файла для записи лога
    """
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message)
    else:
        print(message, end="")


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

# demonstrate_decorators()