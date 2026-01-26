from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot import bot
from config import Config
from database import save_user, save_request, get_all_users
from keyboards import main_menu

router = Router()

@router.message(commands=['start'])
async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name or ""
    await save_user(user_id, username, full_name)
    
    welcome_text = (
        "Добро пожаловать в Asia Expert! 🌴\n"
        "Мы — крупнейший консьерж-сервис для экспатов в Азии. Наша команда берет на себя все организационные вопросы в Северном Гоа: "
        "от поиска виллы и няни до обмена валют и доставки цветов. Ваша уверенность и комфорт — наша главная цель."
    )
    await message.answer(welcome_text)
    await message.answer("Выберите необходимую услугу:", reply_markup=main_menu())

service_map = {
    "service_rent_house": "Аренда жилья",
    "service_rent_bike": "Аренда байка",
    "service_rent_car": "Аренда авто",
    "service_exchange": "Обмен валюты / USDT",
    "service_taxi": "Такси",
    "service_food_delivery": "Доставка еды",
    "service_pharmacy": "Аптека на дом",
    "service_nanny": "Няня",
    "service_flowers": "Доставка цветов",
    "service_question": "Задать вопрос"
}

@router.callback_query(F.data.startswith("service_"))
async def service_handler(call: CallbackQuery):
    service_type = service_map.get(call.data, "Неизвестная услуга")
    user_id = call.from_user.id
    await save_request(user_id, service_type)
    
    await call.message.answer("Заявка принята! Менеджер по Северному Гоа свяжется с вами в личных сообщениях в ближайшее время.")
    
    log_text = (
        f"🔔 НОВАЯ ЗАЯВКА — {service_type}\n"
        f"• Клиент: @{call.from_user.username}\n"
        f"• Имя: {call.from_user.full_name}\n"
        f"• Локация: {Config.LOCATION_NAME}"
    )
    await bot.send_message(Config.ADMIN_CHANNEL_ID, log_text)
    await call.answer()

@router.message(commands=['send'])
async def broadcast_handler(message: Message):
    if message.from_user.id != Config.ADMIN_ID:
        await message.answer("Доступ запрещён.")
        return
    
    text = message.text.replace('/send ', '')
    if not text:
        await message.answer("Укажите текст после /send")
        return
    
    users = await get_all_users()
    sent = 0
    errors = 0
    for user_id in users:
        try:
            await bot.send_message(int(user_id), text)
            sent += 1
            await asyncio.sleep(0.05)  # ~20 сообщений в секунду
        except:
            errors += 1
    
    await message.answer(f"Рассылка завершена: отправлено {sent}, ошибок {errors}")