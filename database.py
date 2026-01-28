import firebase_admin
from firebase_admin import credentials, firestore_async
from config import Config
import json
from datetime import datetime

db = None

def init_firebase():
    global db
    # cred = credentials.Certificate(json.loads(Config.FIREBASE_CREDENTIALS_PATH))
    cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore_async.client()

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