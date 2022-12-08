"""Dependencies that used all across the app
"""

import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.config import Config

config = Config()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    filename=config.logs_path/Path("logs.txt")
)


# Bot init
bot = Bot(token=config.bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
