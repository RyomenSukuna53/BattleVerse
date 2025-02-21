import sys
import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.handlers import MessageHandler, CallbackQueryHandler


# Environment Variables
API_ID = os.getenv("27548865")
API_HASH = os.getenv("db07e06a5eb288c706d4df697b71ab61")
TOKEN = os.getenv("7708237172:AAFM9Yag7L6YiLe7eK7PcS4j3MW-o4OoYh4")
SUPPORT_CHAT = os.getenv("shoadow_battle_verse07", "hgbotsupportgroup")
BOT_OWNER_ID = int(os.getenv("6239769036", "7074356361"))

if not (API_ID and API_HASH and TOKEN):
    sys.exit("API_ID, API_HASH, and TOKEN must be set in environment variables.")

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
                                                    logging.StreamHandler()], format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOGGER = logging.getLogger(__name__)



# Pyrogram Client Setup
bot = Client(
    "Bot",  # Name of the session
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="Modules")  # Specify the plugin directory here
)
