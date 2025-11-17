"""Главный модуль запуска программы, который отвечает за основную логику проекта
и связывает функциональности между собой."""

from config import TRANSACTIONS_CSV_FILE_PATH, TRANSACTIONS_EXCEL_FILE_PATH, TRANSACTIONS_JSON_FILE_PATH
from src.final_modul import (
    extract_categories_from_transactions,
    filter_rub_transactions,
    format_transaction_display,
    get_search_suggestions,
    get_status_input_with_suggestions,
    get_user_choice,
    handle_empty_status_filter,
    process_bank_operations,
    process_bank_search,
    sort_by_date,
)
from src.read_json_csv_excel import (
    FileLoadError,
    FileReadError,
    load_transactions,
    read_transactions_csv,
    read_transactions_excel,
)


def main() -> None:
    """Основная функция программы"""

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = get_user_choice("Ваш выбор: ", ["1", "2", "3"])

    if file_choice == "1":
        print("Для обработки выбран JSON-файл.")
        file_path = TRANSACTIONS_JSON_FILE_PATH
        try:
            transactions = load_transactions(file_path)
        except FileLoadError as e:
            print(f"Ошибка загрузки JSON файла: {e}")
            return
    elif file_choice == "2":
        print("Для обработки выбран CSV-файл.")
        file_path = TRANSACTIONS_CSV_FILE_PATH
        try:
            transactions = read_transactions_csv(file_path)
        except FileReadError as e:
            print(f"Ошибка загрузки CSV файла: {e}")
            return
    else:  # file_choice == '3'
        print("Для обработки выбран XLSX-файл.")
        file_path = TRANSACTIONS_EXCEL_FILE_PATH
        try:
            transactions = read_transactions_excel(file_path)
        except FileReadError as e:
            print(f"Ошибка загрузки Excel файла: {e}")
            return

    # Проверка загрузки данных
    if not transactions:
        print("Не удалось загрузить транзакции или файл пуст")
        return

    # Фильтрация по статусу
    status_processing_complete = False
    filtered_transactions = []

    while not status_processing_complete:
        # Используем улучшенную функцию с подсказками
        selected_status = get_status_input_with_suggestions(transactions)
        filtered_transactions = process_bank_search(transactions, selected_status)

        if filtered_transactions:
            print(f'Операции отфильтрованы по статусу "{selected_status}"')
            print(f"Найдено операций: {len(filtered_transactions)}")
            status_processing_complete = True
        else:
            # Обрабатываем ситуацию, когда транзакций с выбранным статусом нет
            result = handle_empty_status_filter(transactions, selected_status)

            if result["action"] == "exit":
                print("Завершение программы...")
                return
            else:
                filtered_transactions = result["transactions"]
                status_processing_complete = True

    # Сортировка по дате
    sort_choice = get_user_choice("\nОтсортировать операции по дате? Да/Нет: ", ["да", "нет", "д", "н"]).lower()

    if sort_choice in ["да", "д"]:
        order_choice = get_user_choice(
            "Отсортировать по возрастанию или по убыванию? ",
            ["по возрастанию", "по убыванию", "возрастанию", "убыванию"],
        )

        reverse = order_choice in ["по убыванию", "убыванию"]
        filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse)
        order_text = "по убыванию" if reverse else "по возрастанию"
        print(f"Операции отсортированы {order_text}")
    else:
        print("Сортировка по дате не применена")

    # Фильтрация рублевых транзакций
    rub_choice = get_user_choice("\nВыводить только рублевые транзакции? Да/Нет: ", ["да", "нет", "д", "н"])

    if rub_choice in ["да", "д"]:
        filtered_transactions = filter_rub_transactions(filtered_transactions)
        print("Выводятся только рублевые транзакции")
        print(f"Осталось операций: {len(filtered_transactions)}")
    else:
        print("Выводятся транзакции в любой валюте")

    # Проверка после фильтрации рублевых транзакций
    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Поиск по описанию
    search_choice = get_user_choice(
        "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: ", ["да", "нет", "д", "н"]
    )

    if search_choice in ["да", "д"]:
        search_completed = False

        # Получаем подсказки по популярным словам (только если есть транзакции)
        suggestions = []
        if filtered_transactions:
            suggestions = get_search_suggestions(filtered_transactions)

        while not search_completed:
            # Показываем подсказки, если они есть
            if suggestions:
                print(f"\nНаиболее часто встречающиеся слова в описаниях: {', '.join(suggestions)}")

            search_word = input("Введите слово для поиска в описании: ").strip()

            if not search_word:
                print("Поисковый запрос не может быть пустым. Попробуйте снова.")
                continue

            # Выполняем поиск
            search_results = process_bank_search(filtered_transactions, search_word)

            if search_results:
                # Если найдены результаты, применяем фильтр
                filtered_transactions = search_results
                print(f'Операции отфильтрованы по слову "{search_word}"')
                print(f"Найдено операций: {len(filtered_transactions)}")
                search_completed = True
            else:
                # Если результатов нет, предлагаем выбор
                print(f'\nПо запросу "{search_word}" не найдено ни одной транзакции.')
                print("Выберите действие:")
                print("1. Ввести другое слово для поиска")
                print("2. Продолжить без фильтрации по описанию")

                retry_choice = get_user_choice("Ваш выбор (1 или 2): ", ["1", "2"])

                if retry_choice == "1":
                    # Продолжаем цикл с новым запросом
                    print("Попробуйте ввести другое слово.")
                    continue
                else:
                    # Выходим из цикла без применения фильтра
                    print("Фильтрация по описанию отменена.")
                    search_completed = True
    else:
        print("Фильтрация по ключевому слову не применена")

    # Финальная проверка на пустую выборку
    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)},")
    category_stats = process_bank_operations(
        filtered_transactions, extract_categories_from_transactions(filtered_transactions)
    )

    print("\nв том числе по категориям:\n")
    for category, count in category_stats.items():
        print(f"  - {category}: {count}")

    print()
    print("-" * 60)

    for i, transaction in enumerate(filtered_transactions, 1):
        print(format_transaction_display(transaction))
        print("-" * 60)


if __name__ == "__main__":
    main()
