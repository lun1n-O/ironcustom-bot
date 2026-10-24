import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

TOKEN = "8822699244:AAGL9kiow28TjAXmpX7OYx_Dmgf0sgHgLU8"
MANAGER_ID = 1220308552

bot = Bot(token=TOKEN)
dp = Dispatcher()

class UserStates(StatesGroup):
    waiting_for_order = State()

def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛠 Services & Prices", callback_data="services")],
        [InlineKeyboardButton(text="💬 Order / Consultation", callback_data="order")],
        [InlineKeyboardButton(text="📍 Contacts", callback_data="contacts")]
    ])

def get_services_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💻 Turnkey PC Build — 1500 RUB", callback_data="serv_pc")],
        [InlineKeyboardButton(text="🧹 Cleaning & Maintenance — from 500 RUB", callback_data="serv_clean")],
        [InlineKeyboardButton(text="🎮 Console Maintenance — from 500 RUB", callback_data="serv_console")],
        [InlineKeyboardButton(text="◀️ Back", callback_data="main_menu")]
    ])

@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "Hello! This is the **IRONCUSTOM** service center 🛠\n\n"
        "We specialize in professional PC assembly, custom maintenance, and console repair.\n"
        "Please choose a section below:"
    )
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@dp.callback_query(F.data == "main_menu")
async def cb_main(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text("IRONCUSTOM Main Menu:", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "services")
async def cb_services(call: CallbackQuery):
    await call.answer()
    text = "Our services and price list:"
    await call.message.edit_text(text, reply_markup=get_services_keyboard())

@dp.callback_query(F.data.startswith("serv_"))
async def cb_serv_detail(call: CallbackQuery):
    await call.answer()
    info = {
        "serv_pc": "💻 **Turnkey PC Assembly (1500 RUB)**:\nComponent selection, assembly, cable management, OS and driver installation, stress testing.",
        "serv_clean": "🧹 **Cleaning & Maintenance (from 500 RUB)**:\nFull disassembly, thermal paste/pad replacement, dust cleaning.",
        "serv_console": "🎮 **Console Maintenance (from 500 RUB)**:\nPlayStation/Xbox cleaning, thermal paste replacement, noise and overheating elimination."
    }
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Place an Order", callback_data="order")],
        [InlineKeyboardButton(text="◀️ Back to Services", callback_data="services")]
    ])
    await call.message.edit_text(info.get(call.data, ""), reply_markup=kb, parse_mode="Markdown")

@dp.callback_query(F.data == "contacts")
async def cb_contacts(call: CallbackQuery):
    await call.answer()
    text = (
        "📍 **IRONCUSTOM Contacts**:\n\n"
        "• On-site service available in the city\n"
        "• Direct master contact: @lun1n_l\n\n"
        "Click 'Order' to leave a request!"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Message Master", url="https://t.me/lun1n_l")],
        [InlineKeyboardButton(text="◀️ Main Menu", callback_data="main_menu")]
    ])
    await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query(F.data == "order")
async def cb_order(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(UserStates.waiting_for_order)
    await call.message.answer("Please describe your task or question in a single message (e.g., need a PC build up to 60000 RUB):")

@dp.message(UserStates.waiting_for_order)
async def process_order(message: Message, state: FSMContext):
    await state.clear()
    user = message.from_user
    username = f"@{user.username}" if user.username else "no username"
    
    # Безопасный текст без разметки Markdown, чтобы ничего не ломалось
    manager_text = (
        "📥 New request in IRONCUSTOM!\n\n"
        f"From: {user.full_name} ({username})\n"
        f"ID: {user.id}\n\n"
        "Message:\n"
        f"{message.text}"
    )
    
    try:
        await bot.send_message(MANAGER_ID, manager_text)
    except Exception as e:
        logging.error(f"Failed to send message to manager: {e}")

    await message.answer("Thank you! Your request has been accepted. The master will contact you soon 🙌")

async def handle(request):
    return web.Response(text="IRONCUSTOM Bot is running 24/7!")

async def main():
    logging.basicConfig(level=logging.INFO)
    
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    print("🚀 IRONCUSTOM bot successfully started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
