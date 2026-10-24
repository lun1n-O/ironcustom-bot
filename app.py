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
        [InlineKeyboardButton(text="🛠 Услуги и цены", callback_data="services")],
        [InlineKeyboardButton(text="💬 Заказать / Консультация", callback_data="order")],
        [InlineKeyboardButton(text="📍 Контакты", callback_data="contacts")]
    ])

def get_services_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💻 Сборка ПК под ключ — 1500 ₽", callback_data="serv_pc")],
        [InlineKeyboardButton(text="🧹 Чистка и обслуживание — от 500 ₽", callback_data="serv_clean")],
        [InlineKeyboardButton(text="🎮 Обслуживание консолей — от 500 ₽", callback_data="serv_console")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])

@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "Привет! Это сервисный центр **IRONCUSTOM** 🛠\n\n"
        "Мы занимаемся профессиональной сборкой ПК, кастомным обслуживанием и ремонтом консолей.\n"
        "Выберите интересующий вас раздел:"
    )
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@dp.callback_query(F.data == "main_menu")
async def cb_main(call: CallbackQuery):
    await call.message.edit_text("Главное меню IRONCUSTOM:", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "services")
async def cb_services(call: CallbackQuery):
    text = "Наши услуги и прайс-лист:"
    await call.message.edit_text(text, reply_markup=get_services_keyboard())

@dp.callback_query(F.data.startswith("serv_"))
async def cb_serv_detail(call: CallbackQuery):
    info = {
        "serv_pc": "💻 **Сборка ПК под ключ (1500 ₽)**:\nПодбор комплектующих, сборка, кабель-менеджмент, установка ОС и драйверов, стресс-тесты.",
        "serv_clean": "🧹 **Чистка и обслуживание (от 500 ₽)**:\nПолная разборка, замена термопасты/термопрокладок, очистка от пыли.",
        "serv_console": "🎮 **Обслуживание консолей (от 500 ₽)**:\nЧистка PlayStation/Xbox, замена термопасты, устранение шума и перегрева."
    }
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Оформить заявку", callback_data="order")],
        [InlineKeyboardButton(text="◀️ Назад к услугам", callback_data="services")]
    ])
    await call.message.edit_text(info.get(call.data, ""), reply_markup=kb, parse_mode="Markdown")

@dp.callback_query(F.data == "contacts")
async def cb_contacts(call: CallbackQuery):
    text = (
        "📍 **Контакты IRONCUSTOM**:\n\n"
        "• Работаем с выездом на дом по городу\n"
        "• Прямой контакт мастера: @lun1n_l\n\n"
        "Нажмите «Заказать», чтобы оставить заявку!"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Написать мастеру", url="https://t.me/lun1n_l")],
        [InlineKeyboardButton(text="◀️ Главное меню", callback_data="main_menu")]
    ])
    await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query(F.data == "order")
async def cb_order(call: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.waiting_for_order)
    await call.message.answer("Опишите вашу задачу или вопрос в одном сообщении (например: нужна сборка ПК до 60 000 руб):")

@dp.message(UserStates.waiting_for_order)
async def process_order(message: Message, state: FSMContext):
    await state.clear()
    user = message.from_user
    username = f"@{user.username}" if user.username else "без username"
    
    manager_text = (
        f"📥 **Новая заявка в IRONCUSTOM!**\n\n"
        f"От: {user.full_name} ({username})\n"
        f"ID: `{user.id}`\n\n"
        f"**Сообщение:**\n{message.text}"
    )
    await bot.send_message(MANAGER_ID, manager_text, parse_mode="Markdown")
    await message.answer("Спасибо! Ваша заявка принята. Мастер скоро свяжется с вами 🙌")

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
    
    print("🚀 Бот IRONCUSTOM успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
