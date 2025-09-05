"""Главный модуль запуска программы."""

from src.masks import get_mask_account, get_mask_card_number

if __name__ == "__main__":
    # Вызываем и выводим результат
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))
