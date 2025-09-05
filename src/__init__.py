"""Пакет функций для маскировки номеров банковской карты и лицевого счета."""

from .masks import get_mask_card_number, get_mask_account

__all__ = ["get_mask_card_number", "get_mask_account"]
