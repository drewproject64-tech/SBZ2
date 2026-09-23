from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from .db import SessionLocal, LiveItem, get_items, list_categories, search_items
from .keyboards import back_menu, category_menu, main_menu, search_menu

router = Router()


class SearchState(StatesGroup):
    waiting_query = State()


def item_text(item: LiveItem, index: int) -> str:
    return (
        f"{index}. <b>{item.name}</b>\n"
        f"{item.description}\n"
        f"<b>Category:</b> {item.category}"
    )


def home_text() -> str:
    return (
        "👋 <b>Welcome to SB24GZ - Live</b>\n\n"
        "Explore live and featured Telegram content from one simple directory.\n\n"
        "Choose an option below:"
    )


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(home_text(), reply_markup=main_menu())


@router.message(Command("help"))
async def help_cmd(message: Message) -> None:
    await message.answer(
        "ℹ️ <b>About SB24GZ - Live</b>\n\n"
        "• Live Channels — explore live listings.\n"
        "• Search — find listings by keyword.\n"
        "• Featured — view selected listings.\n\n"
        "The main features work directly inside Telegram.",
        reply_markup=main_menu(),
    )


@router.message(Command("cancel"))
async def cancel_cmd(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("✅ Cancelled.", reply_markup=main_menu())


@router.callback_query(F.data == "main")
async def main_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    try:
        await call.message.edit_text(home_text(), reply_markup=main_menu())
    except TelegramBadRequest:
        await call.message.answer(home_text(), reply_markup=main_menu())
    await call.answer()


@router.callback_query(F.data == "live")
async def live_callback(call: CallbackQuery) -> None:
    async with SessionLocal() as session:
        categories = await list_categories(session)
    if not categories:
        await call.message.edit_text(
            "🔴 <b>Live Channels</b>\n\nNo live listings are available yet.",
            reply_markup=back_menu(),
        )
    else:
        await call.message.edit_text(
            "🔴 <b>Live Channels</b>\n\nChoose a category:",
            reply_markup=category_menu(categories),
        )
    await call.answer()


@router.callback_query(F.data == "search")
async def search_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SearchState.waiting_query)
    await call.message.edit_text(
        "🔎 <b>Search</b>\n\n"
        "Enter a keyword such as <code>news</code>, <code>sports</code>, or <code>live</code>.\n\n"
        "Use /cancel to stop.",
        reply_markup=back_menu(),
    )
    await call.answer()


@router.message(SearchState.waiting_query)
async def process_search(message: Message, state: FSMContext) -> None:
    query = (message.text or "").strip()
    if not query:
        await message.answer("Please enter a keyword.", reply_markup=back_menu())
        return
    if len(query) > 80:
        await message.answer("Please keep the search to 80 characters or fewer.", reply_markup=back_menu())
        return

    async with SessionLocal() as session:
        results = await search_items(session, query)

    await state.clear()

    if not results:
        await message.answer(
            f'No results found for "<b>{query}</b>". Try another keyword.',
            reply_markup=search_menu(),
        )
        return

    body = [f"🔎 <b>Results for:</b> {query}", ""]
    for index, item in enumerate(results, 1):
        body.extend([item_text(item, index), ""])
    await message.answer("\n".join(body), reply_markup=search_menu())


@router.callback_query(F.data.startswith("cat:"))
async def category_callback(call: CallbackQuery) -> None:
    category = call.data.split(":", 1)[1]
    async with SessionLocal() as session:
        results = await get_items(session, category=category)

    if not results:
        text = f"🔴 <b>{category}</b>\n\nNo listings are available in this category yet."
    else:
        body = [f"🔴 <b>{category}</b>", ""]
        for index, item in enumerate(results, 1):
            body.extend([item_text(item, index), ""])
        text = "\n".join(body)

    await call.message.edit_text(text, reply_markup=back_menu())
    await call.answer()


@router.callback_query(F.data == "featured")
async def featured_callback(call: CallbackQuery) -> None:
    async with SessionLocal() as session:
        results = await get_items(session, featured=True)

    if not results:
        text = "⭐ <b>Featured</b>\n\nNo featured listings are available yet."
    else:
        body = ["⭐ <b>Featured</b>", ""]
        for index, item in enumerate(results, 1):
            body.extend([item_text(item, index), ""])
        text = "\n".join(body)

    await call.message.edit_text(text, reply_markup=back_menu())
    await call.answer()


@router.callback_query()
async def unknown_callback(call: CallbackQuery) -> None:
    await call.answer("Please return to the main menu.", show_alert=True)
