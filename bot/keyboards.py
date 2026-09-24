from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔢 Count Text", callback_data="count")],
        [InlineKeyboardButton(text="🧹 Clean Text", callback_data="clean")],
        [InlineKeyboardButton(text="🔤 Change Case", callback_data="case")],
    ])


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Main Menu", callback_data="main")]
    ])


def case_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="UPPERCASE", callback_data="case:upper")],
        [InlineKeyboardButton(text="lowercase", callback_data="case:lower")],
        [InlineKeyboardButton(text="Title Case", callback_data="case:title")],
        [InlineKeyboardButton(text="⬅️ Main Menu", callback_data="main")],
    ])
