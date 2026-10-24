import asyncio
import logging
import re
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

# -------------------------------------------------------------
# НАСТРОЙКИ (Вставлены твои данные)
# -------------------------------------------------------------
TOKEN = "8822699244:AAGL9kiow28TjAXmpX7OYx_Dmgf0sgHgLU8"
MANAGER_ID = 1220308552

bot = Bot(token=TOKEN)
dp = Dispatcher()

# -------------------------------------------------------------
# СОСТОЯНИЯ (FSM)
# -------------------------------------------------------------
class UserStates(StatesGroup):
    waiting_for_order = State()  # Ожидание описания и фото устройства от клиента

# -------------------------------------------------------------
# КЛАВИАТУРЫ
# -------------------------------------------------------------
def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛠 Услуги и цены", callback_data="services_menu")],
        [InlineKeyboardButton(text="💬 Заказать / Консультация", callback_data="ask_manager")],
        [InlineKeyboardButton(text="📍 Контакты", callback_data="contacts")]
    ])

def get_services_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖥 Сборка ПК под ключ", callback_data="srv_pc_build")],
        [InlineKeyboardButton(text="🧽 Детейлинг и чистка ПК", callback_data="srv_pc_clean")],
        [InlineKeyboardButton(text="🎮 Чистка консолей (PS / Xbox)", callback_data="srv_consoles")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
    ])

def get_cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")]
    ])

# -------------------------------------------------------------
# 1. ГЛАВНОЕ МЕНЮ И СТАРТ
# -------------------------------------------------------------
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    welcome_text = (
        "👋 **Добро пожаловать в IRONCUSTOM!**\n\n"
        "Мы занимаемся профессиональной сборкой компьютеров, а также глубоким "
        "детейлингом (чисткой, заменой термопасты/термопрокладок) ПК и игровых приставок.\n\n"
        "Выберите интересующий раздел ниже:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "👋 **Главное меню IRONCUSTOM:**\n\nВыберите нужный раздел:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

# -------------------------------------------------------------
# 2. РАЗДЕЛ УСЛУГ И ЦЕН
# -------------------------------------------------------------
@dp.callback_query(F.data == "services_menu")
async def process_services(callback: CallbackQuery):
    await callback.message.edit_text(
        "📦 **Наши услуги и цены IRONCUSTOM:**\n\n"
        "Выберите категорию, чтобы узнать подробности:",
        reply_markup=get_services_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "srv_pc_build")
async def srv_pc_build(callback: CallbackQuery):
    text = (
        "🖥 **Сборка ПК под ключ:**\n\n"
        "• Подбор комплектующих под ваш бюджет и задачи\n"
        "• Аккуратный кабель-менеджмент\n"
        "• Стресс-тестирование и настройка системы\n\n"
        "💰 *Стоимость:* 1500 рублей"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Заказать сборку", callback_data="ask_manager")],
        [InlineKeyboardButton(text="🔙 К списку услуг", callback_data="services_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "srv_pc_clean")
async def srv_pc_clean(callback: CallbackQuery):
    text = (
        "🧽 **Детейлинг и чистка ПК:**\n\n"
        "• Полная разборка и очистка от пыли\n"
        "• Замена термопасты (процессор, видеокарта)\n"
        "• Замена термопрокладок (при необходимости)\n"
        "• Аккуратная укладка проводов\n\n"
        "💰 *Стоимость:* от 500 рублей"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Записаться на чистку", callback_data="ask_manager")],
        [InlineKeyboardButton(text="🔙 К списку услуг", callback_data="services_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "srv_consoles")
async def srv_consoles(callback: CallbackQuery):
    text = (
        "🎮 **Обслуживание консолей (PS4 / PS5 / Xbox):**\n\n"
        "• Чистка системы охлаждения от пыли и шерсти\n"
        "• Замена термопасты или жидкого металла (PS5)\n"
        "• Очистка блока питания и кулера\n\n"
        "💰 *Стоимость:* от 500 рублей"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Записаться с консолью", callback_data="ask_manager")],
        [InlineKeyboardButton(text="🔙 К списку услуг", callback_data="services_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

# -------------------------------------------------------------
# 3. КОНТАКТЫ
# -------------------------------------------------------------
@dp.callback_query(F.data == "contacts")
async def process_contacts(callback: CallbackQuery):
    text = (
        "📍 **Контакты IRONCUSTOM:**\n\n"
        "🏠 **Формат работы:** Работаем на дому\n"
        "💬 **Связь с мастером:** @lun1n_l"
    )
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

# -------------------------------------------------------------
# 4. ДИАЛОГ С МАСТЕРОМ (КЛИЕНТ -> МАСТЕР)
# -------------------------------------------------------------
@dp.callback_query(F.data == "ask_manager")
async def ask_manager_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.waiting_for_order)
    text = (
        "✍️ **Опишите вашу задачу:**\n\n"
        "• Какое у вас устройство (модель ПК, видеокарта или консоль)?\n"
        "• Какая услуга требуется (сборка, чистка, греется/шумит)?\n"
        "📸 *Вы можете прикрепить фото или скриншот устройства.*"
    )
    await callback.message.edit_text(text, reply_markup=get_cancel_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "cancel_action")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Действие отменено.", reply_markup=get_main_keyboard())
    await callback.answer()

# Получение запроса от клиента
@dp.message(UserStates.waiting_for_order, F.from_user.id != MANAGER_ID)
async def process_user_order(message: Message, state: FSMContext):
    user = message.from_user
    username_info = f"(@{user.username})" if user.username else "(без юзернейма)"
    
    header = (
        f"🚨 **Новая заявка в IRONCUSTOM!**\n"
        f"👤 Клиент: {user.full_name} {username_info}\n"
        f"🆔 ID: `{user.id}`\n"
        f"-----------------------------------"
    )
    
    # Пересылаем текст или медиафайл мастеру
    if message.text:
        await bot.send_message(MANAGER_ID, f"{header}\n\n💬 **Описание:**\n{message.text}", parse_mode="Markdown")
    else:
        await bot.send_message(MANAGER_ID, header, parse_mode="Markdown")
        await message.copy_to(chat_id=MANAGER_ID)

    await state.clear()
    
    await message.answer(
        "✅ **Заявка принята!**\nМастер изучит информацию и ответит вам в ближайшее время.",
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )

# -------------------------------------------------------------
# 5. ОТВЕТ МАСТЕРА КЛИЕНТУ
# -------------------------------------------------------------
@dp.message(F.from_user.id == MANAGER_ID)
async def reply_from_manager(message: Message):
    if not message.reply_to_message:
        await message.answer(
            "⚠️ Чтобы ответить клиенту, нажмите на его заявку и выберите **«Ответить» (Reply)** в Telegram."
        )
        return

    target_msg = message.reply_to_message
    raw_text = target_msg.text or target_msg.caption or ""
    
    match = re.search(r"ID:\s*`(\d+)`", raw_text)
    if not match:
        await message.answer("❌ Не найден ID клиента. Убедитесь, что отвечаете на карточку заявки с ID.")
        return

    client_id = int(match.group(1))

    try:
        if message.text:
            await bot.send_message(client_id, f"👨‍🔧 **Ответ от IRONCUSTOM:**\n\n{message.text}", parse_mode="Markdown")
        else:
            await bot.send_message(client_id, "👨‍🔧 **Ответ от IRONCUSTOM:**")
            await message.copy_to(chat_id=client_id)
            
        await message.answer("✅ Ответ успешно отправлен клиенту!")
    except Exception as e:
        await message.answer(f"❌ Ошибка отправки:\n`{e}`", parse_mode="Markdown")

# -------------------------------------------------------------
# ЗАПУСК
# -------------------------------------------------------------
async def main():
    logging.basicConfig(level=logging.INFO)
    print("🚀 Бот IRONCUSTOM успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
