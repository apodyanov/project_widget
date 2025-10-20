import logging
from venv import logger


logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/masks.log', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


"""Модуль выполняющий маскировку номера банковской карты и счета клиента."""


def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты показывает
    первые шесть и последние четыре цифры."""
    try:
        logger.info(f'Проверка корректного ввода номера карты')
        if not card_number.isdigit():
            logger.error(f'Не корректный ввод номера карты')
            raise ValueError("Номер карты должен содержать только цифры")

        if len(card_number) != 16:
            logger.error(f'Не корректный ввод номера карты')
            raise ValueError("Номер карты должен быть только из 16 цифр")

        logger.info(f'Формирование маски номера карты')
        # Разбиваем на группы по 4 цифры
        part1 = card_number[:4]
        part2 = card_number[4:6]  # Первые 2 цифры второй группы
        part3 = "****"  # Полностью скрытая третья группа
        part4 = card_number[-4:]  # Последние 4 цифры

        return f"{part1} {part2}** {part3} {part4}"
    except ValueError as ex:
        logger.error(f'Произошла ошибка: {ex}')
        return f'Произошла ошибка'



def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета клиента показывает
    только последние четыре цифры номера счета."""

    try:
        logger.info(f'Проверка корректного ввода счета')
        if not account_number.isdigit():
            logger.error(f'Не корректный ввод номера счета')
            raise ValueError("Номер счета должен содержать только цифры")

        logger.info(f'Проверка на минимально допустимое количество цифр счета')
        if len(account_number) < 4:
            logger.error(f'Номер счета должен содержать минимум 4 цифры')
            raise ValueError("Номер счета должен содержать минимум 4 цифры")

        # Показываем только последние 4 цифры
        logger.info(f'Формирование маски номера счета')
        return f"**{account_number[-4:]}"
    except ValueError as ex:
        logger.error(f'Произошла ошибка: {ex}')
        return f'Произошла ошибка'
