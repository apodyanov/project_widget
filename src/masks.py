"""Модуль выполняющий маскировку номера банковской карты и счета клиента."""


def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты показывает первые шесть и последние четыре цифры.

    Args:
        card_number: Номер банковской карты вводится строкой (16 цифр)

    Returns:
        Маску номера банковской карты в формате: XXXX XX** **** XXXX

    Raises:
        ValueError: Если номер карты не 16 цифр или содержит не только цифры

    Examples:
        >>> get_mask_card_number("7000792289606361")
        '7000 79** **** 6361'
    """
    if not card_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    if len(card_number) != 16:
        raise ValueError("Номер карты должен быть только из 16 цифр")

    # Разбиваем на группы по 4 цифры
    part1 = card_number[:4]
    part2 = card_number[4:6]  # Первые 2 цифры второй группы
    part3 = "****"  # Полностью скрытая третья группа
    part4 = card_number[-4:]  # Последние 4 цифры

    return f"{part1} {part2}** {part3} {part4}"


def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета клиента показывает только последние четыре цифры номера счета.

    Args:
        account_number: Номер банковского счета вводится строкой

    Returns:
        Маску номера банковского счета клиента в формате: **XXXX

    Raises:
        ValueError: Если номер счета слишком короткий или содержит не только цифры

    Examples:
        >>> get_mask_account("73654108430135874305")
        '**4305'
    """
    if not account_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    # Показываем только последние 4 цифры
    return f"**{account_number[-4:]}"
