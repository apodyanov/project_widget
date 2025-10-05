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
