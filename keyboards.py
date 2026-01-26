from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu():
    kb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="🏠 Аренда жилья", callback_data="service_rent_house"),
        InlineKeyboardButton(text="🏍 Аренда байка", callback_data="service_rent_bike"),
        InlineKeyboardButton(text="🚗 Аренда авто", callback_data="service_rent_car"),
        InlineKeyboardButton(text="💸 Обмен валюты / USDT", callback_data="service_exchange"),
        InlineKeyboardButton(text="🚕 Такси", callback_data="service_taxi"),
        InlineKeyboardButton(text="🍕 Доставка еды", callback_data="service_food_delivery"),
        InlineKeyboardButton(text="💊 Аптека на дом", callback_data="service_pharmacy"),
        InlineKeyboardButton(text="👶 Няня", callback_data="service_nanny"),
        InlineKeyboardButton(text="💐 Доставка цветов", callback_data="service_flowers"),
        InlineKeyboardButton(text="❓ Задать вопрос", callback_data="service_question")
    ]
    for button in buttons:
        kb.add(button)
    kb.adjust(2)  # 2 кнопки в ряд
    return kb.as_markup()