from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_ID = int(os.getenv('ADMIN_ID'))
    ADMIN_CHANNEL_ID = int(os.getenv('ADMIN_CHANNEL_ID'))
    LOCATION_NAME = os.getenv('LOCATION_NAME', 'Северное Гоа')
    # FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS')  # путь к JSON или содержимое
    FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "/etc/secrets/firebase.json")
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    PORT = int(os.getenv('PORT', 8080))







# FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "/etc/secrets/firebase.json")