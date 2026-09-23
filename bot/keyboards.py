from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔴 Live Channels", callback_data="live")],
        [InlineKeyboardButton(text="🔎 Search", callback_data="search")],
        [InlineKeyboardButton(text="⭐ Featured", callback_data="featured")],
    ])


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Main Menu", callback_data="main")]
    ])


def category_menu(categories: list[str]) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=f"📁 {c}", callback_data=f"cat:{c}")] for c in categories]
    rows.append([InlineKeyboardButton(text="⬅️ Main Menu", callback_data="main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def search_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Search Again", callback_data="search")],
        [InlineKeyboardButton(text="⬅️ Main Menu", callback_data="main")],
    ])
