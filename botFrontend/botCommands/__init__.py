from aiogram import Bot, Dispatcher
import logging
from dotenv import load_dotenv
import os



load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

from . import commands
