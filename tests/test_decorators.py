"""Тесты для модуля decorators."""

import os
import tempfile

import pytest

from src.decorators import log


class TestLogDecorator:
    """Тест декоратора log."""

    def test_log_to_console_success(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест успешного логирования в консоль."""

        @log()
        def add(a: int, b: int) -> int:
            return a + b

        result = add(2, 3)

        # Проверка результата
        assert result == 5

        # Проверка вывода в консоль
        captured = capsys.readouterr()
        assert "add ok" in captured.out

    def test_log_to_console_error(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест логирования функции в консоль с ошибкой."""

        @log()
        def divide(a: int, b: int) -> float:
            return a / b

        # Тест деления на ноль
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        # Проверка вывода в консоль
        captured = capsys.readouterr()
        assert "divide error: ZeroDivisionError" in captured.out
        assert "Inputs: (10, 0)" in captured.out

    def test_log_to_file_success(self) -> None:
        """Тест логирования успешного выполнения функции в файл."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            filename = f.name  # type: ignore

        try:

            @log(filename=filename)
            def multiply(a: int, b: int) -> int:
                return a * b

            result = multiply(4, 5)

            # Проверка результата функции
            assert result == 20

            # Проверка содержимого файла
            with open(filename, "r", encoding="utf-8") as f:  # type: ignore
                content = f.read()
                assert "multiply ok" in content

        finally:
            # Удаление
            if os.path.exists(filename):
                os.unlink(filename)

    def test_log_to_file_error(self) -> None:
        """Тест записи ошибки функции в файл."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            filename = f.name

        try:

            @log(filename=filename)
            def failing_function(x: int) -> None:
                raise ValueError("Test error")

            # Тест с ошибкой
            with pytest.raises(ValueError, match="Test error"):
                failing_function(42)

            # Проверка содержимого файла
            with open(filename, "r", encoding="utf-8") as f:  # type: ignore
                content = f.read()
                assert "failing_function error: ValueError" in content
                assert "Inputs: (42)" in content

        finally:
            # Удаление
            if os.path.exists(filename):
                os.unlink(filename)

    def test_log_preserves_function_metadata(self) -> None:
        """Тест декоратора на сохранение метаданных."""

        @log()
        def example_func(a: int, b: int = 10) -> int:
            """Пример функции для тестирования."""
            return a + b

        # Проверка сохранения метаданных
        assert example_func.__name__ == "example_func"
        assert example_func.__doc__ == "Пример функции для тестирования."

        # Проверка, что функция продолжает работать корректно
        assert example_func(5) == 15
        assert example_func(5, 20) == 25

    def test_log_with_kwargs(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тестирование лога с ключевыми аргументами."""

        @log()
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"

        result = greet("Alice", greeting="Hi")

        # Проверка результата функции
        assert result == "Hi, Alice!"

        # Проверка вывода в консоль
        captured = capsys.readouterr()
        assert "greet ok" in captured.out

    def test_log_with_complex_arguments(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тестирование с комплексом аргументов."""

        @log()
        def process_data(data: list, options: dict) -> str:
            return f"Processed {len(data)} items"

        result = process_data([1, 2, 3], {"option1": True, "option2": "test"})

        # Проверка результата функции
        assert result == "Processed 3 items"

        # Проверка вывода в консоль на наличие имени функции
        captured = capsys.readouterr()
        assert "process_data ok" in captured.out

    def test_log_empty_arguments(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест логирования функции без аргументов."""

        @log()
        def no_args() -> str:
            return "success"

        result = no_args()

        # Проверка результата функции
        assert result == "success"

        # Проверка вывода в консоль
        captured = capsys.readouterr()
        assert "no_args ok" in captured.out

    def test_log_custom_exception(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест логирования с пользовательским исключением."""

        class CustomError(Exception):
            pass

        @log()
        def raise_custom() -> None:
            raise CustomError("Custom error message")

        # Тест с ошибкой пользователя
        with pytest.raises(CustomError, match="Custom error message"):
            raise_custom()

        # Проверка вывода в консоль
        captured = capsys.readouterr()
        assert "raise_custom error: CustomError" in captured.out
        assert "Inputs: ()" in captured.out

    def test_log_appends_to_existing_file(self) -> None:
        """Тест на логирование в существующий файл, а не перезапись в новый файл."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            filename = f.name
            # Запись существующего содержимого
            f.write("Existing log content\n")

        try:

            @log(filename=filename)
            def test_func() -> str:
                return "result"

            # Вызов функции несколько раз
            test_func()
            test_func()

            # Проверка содержимого файла
            with open(filename, "r", encoding="utf-8") as f:  # type: ignore
                content = f.read()
                lines = content.strip().split("\n")

                # Должен иметь первоначальное содержимое плюс две новых записи
                assert len(lines) >= 3
                assert "Existing log content" in lines[0]
                assert "test_func ok" in lines[1]
                assert "test_func ok" in lines[2]

        finally:
            # Удаление
            if os.path.exists(filename):
                os.unlink(filename)
