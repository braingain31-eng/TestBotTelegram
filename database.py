import firebase_admin
import logging
from firebase_admin import credentials, firestore_async
from config import Config
import json
from datetime import datetime

logger = logging.getLogger(__name__)

db = None

def init_firebase():
    global db
    try:
        # Берем строку JSON из переменной окружения
        # cred_dict = json.loads(Config.FIREBASE_CREDENTIALS)
        cred = credentials.Certificate("/etc/secrets/firebase.json")  # ← передаём словарь, а не строку
        firebase_admin.initialize_app(cred)
        db = firestore_async.client()
        logger.info("Firebase успешно инициализирован из строки JSON")
    except json.JSONDecodeError as e:
        logger.critical(f"Некорректный JSON в FIREBASE_CREDENTIALS: {e}")
        raise
    except Exception as e:
        logger.critical(f"Ошибка инициализации Firebase: {e}", exc_info=True)
        raise

async def save_user(user_id: int, username: str, full_name: str):
    doc_ref = db.collection('users').document(str(user_id))
    await doc_ref.set({
        'username': username,
        'full_name': full_name,
        'registered_at': datetime.utcnow().isoformat()
    }, merge=True)

async def save_request(user_id: int, service_type: str):
    doc_ref = db.collection('requests').document()
    await doc_ref.set({
        'user_id': user_id,
        'service_type': service_type,
        'timestamp': datetime.utcnow().isoformat(),
        'status': 'new'
    })

async def get_all_users():
    users = await db.collection('users').get()
    return [doc.id for doc in users]