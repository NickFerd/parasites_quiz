"""Dependencies that used all across the app
"""

import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

config = Config()

# Bot init
bot = Bot(token=config.bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
