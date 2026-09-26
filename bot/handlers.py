import re
from html import escape

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from .keyboards import back_menu, case_menu, main_menu

router = Router()


class ToolState(StatesGroup):
    waiting_text = State()


def home_text() -> str:
    return (
        "👋 <b>Welcome to SB24GZ Text Bot</b>\n\n"
        "Simple text tools that work directly inside Telegram.\n\n"
        "Choose a tool below:"
    )


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(home_text(), reply_markup=main_menu())


@router.message(Command("help"))
async def help_cmd(message: Message) -> None:
    await message.answer(
        "ℹ️ <b>SB24GZ Text Bot</b>\n\n"
        "• Count Text — count characters, words and lines.\n"
        "• Clean Text — remove extra spaces and blank lines.\n"
        "• Change Case — convert text to upper, lower or title case.\n\n"
        "Everything runs directly inside this bot.",
        reply_markup=main_menu(),
    )


@router.message(Command("cancel"))
async def cancel_cmd(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Cancelled.", reply_markup=main_menu())


@router.callback_query(F.data == "main")
async def main_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text(home_text(), reply_markup=main_menu())
    await call.answer()


@router.callback_query(F.data == "count")
async def count_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ToolState.waiting_text)
    await state.update_data(tool="count")
    await call.message.edit_text(
        "🔢 <b>Count Text</b>\n\nSend the text you want to analyze.",
        reply_markup=back_menu(),
    )
    await call.answer()


@router.callback_query(F.data == "clean")
async def clean_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ToolState.waiting_text)
    await state.update_data(tool="clean")
    await call.message.edit_text(
        "🧹 <b>Clean Text</b>\n\nSend text and I will remove extra spaces and blank lines.",
        reply_markup=back_menu(),
    )
    await call.answer()


@router.callback_query(F.data == "case")
async def case_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ToolState.waiting_text)
    await state.update_data(tool="case")
    await call.message.edit_text(
        "🔤 <b>Change Case</b>\n\nSend the text first, then choose the case.",
        reply_markup=back_menu(),
    )
    await call.answer()


@router.callback_query(F.data.startswith("case:"))
async def case_choice(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    text = data.get("pending_text")
    if not text:
        await call.answer("Send your text first.", show_alert=True)
        return

    mode = call.data.split(":", 1)[1]
    if mode == "upper":
        result = text.upper()
    elif mode == "lower":
        result = text.lower()
    else:
        result = text.title()

    await state.clear()
    await call.message.edit_text(
        f"🔤 <b>Result</b>\n\n<code>{escape(result)}</code>",
        reply_markup=main_menu(),
    )
    await call.answer()


@router.message(ToolState.waiting_text)
async def process_text(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer("Please send some text.", reply_markup=back_menu())
        return
    if len(text) > 4000:
        await message.answer("Please keep the text under 4,000 characters.", reply_markup=back_menu())
        return

    data = await state.get_data()
    tool = data.get("tool")

    if tool == "count":
        words = len(re.findall(r"\S+", text))
        lines = len(text.splitlines())
        characters = len(text)
        characters_no_spaces = len(re.sub(r"\s", "", text))
        await state.clear()
        await message.answer(
            "🔢 <b>Text Count</b>\n\n"
            f"Characters: <b>{characters}</b>\n"
            f"Characters without spaces: <b>{characters_no_spaces}</b>\n"
            f"Words: <b>{words}</b>\n"
            f"Lines: <b>{lines}</b>",
            reply_markup=main_menu(),
        )
        return

    if tool == "clean":
        cleaned_lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
        cleaned = "\n".join(line for line in cleaned_lines if line)
        await state.clear()
        await message.answer(
            f"🧹 <b>Cleaned Text</b>\n\n<code>{escape(cleaned)}</code>",
            reply_markup=main_menu(),
        )
        return

    if tool == "case":
        await state.update_data(pending_text=text)
        await message.answer(
            "Choose the case for your text:",
            reply_markup=case_menu(),
        )
        return

    await state.clear()
    await message.answer("Please choose a tool from the main menu.", reply_markup=main_menu())


@router.callback_query()
async def unknown_callback(call: CallbackQuery) -> None:
    await call.answer("Please choose an option from the menu.", show_alert=True)
