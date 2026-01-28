# main.py
import asyncio
import logging
from flask import Flask, request, abort
from aiogram.types import Update
from config import Config
from bot import bot, dp
from database import init_firebase

app = Flask(__name__)

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик webhook от Telegram (синхронный)"""
    if request.headers.get('content-type') != 'application/json':
        abort(400)

    json_string = request.get_data(as_text=True)
    
    try:
        # update = Update.de_json(json_string, bot)
        update = Update.model_validate_json(json_string)
        if update:
            # Запускаем асинхронную обработку в существующем event loop
            loop = asyncio.get_event_loop()
            loop.run_until_complete(dp.feed_update(bot, update))
    except Exception as e:
        logger.error(f"Ошибка обработки обновления: {type(e).__name__}: {e}", exc_info=True)
        # Опционально: отправить ошибку админу
        # asyncio.create_task(bot.send_message(Config.ADMIN_ID, f"Webhook error: {e}"))

    return 'OK', 200


async def set_webhook():
    """Установка webhook при старте приложения"""
    try:
        await bot.set_webhook(Config.WEBHOOK_URL)
        logger.info(f"Webhook успешно установлен: {Config.WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Ошибка установки webhook: {e}")


def main():
    """Точка входа"""
    init_firebase()
    logger.info(f"----------старт  main")
    # Запускаем установку webhook асинхронно
    # asyncio.run(set_webhook())
    
    # Gunicorn сам запустит Flask, поэтому app.run() здесь не нужен


if __name__ == '__main__':
    # Для локального тестирования (flask run)
    logger.info(f"----------старт  __name__")
    main()
    # app.run(host='0.0.0.0', port=Config.PORT, debug=True)