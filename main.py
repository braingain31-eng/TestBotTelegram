import asyncio
from flask import Flask, request, abort
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from config import Config
from bot import dp, bot
from database import init_firebase

app = Flask(__name__)

# @app.route('/webhook', methods=['POST'])
# async def webhook():
#     if request.headers.get('content-type') != 'application/json':
#         abort(400)
#     json_string = request.get_data(as_text=True)
#     update = Update.parse_raw(json_string)
#     await dp.feed_update(bot, update)
#     return 'OK', 200

@app.route('/webhook', methods=['POST'])
def webhook():                          # ← НЕ async
    if request.headers.get('content-type') != 'application/json':
        abort(400)

    json_string = request.get_data(as_text=True)
    
    try:
        update = Update.de_json(json_string, bot)
        if update:
            # Запускаем асинхронную обработку в синхронном контексте
            asyncio.run(dp.feed_update(bot, update))
    except Exception as e:
        # Логируем ошибку, чтобы видеть в Cloud Run Logs
        print(f"Ошибка обработки обновления: {e}")
        # Можно также отправить себе в админ-канал
        # asyncio.run(bot.send_message(ADMIN_ID, f"Webhook error: {e}"))
    
    return 'OK', 200

async def on_startup():
    webhook_url = Config.WEBHOOK_URL
    await bot.set_webhook(webhook_url)
    print(f"Webhook установлен: {webhook_url}")

if __name__ == '__main__':
    init_firebase()
    # asyncio.run(on_startup())
    # app.run(host='0.0.0.0', port=Config.PORT)