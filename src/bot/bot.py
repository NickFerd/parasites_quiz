"""Bot entry point
"""
import logging
from aiogram.utils import executor

from src.bot.dependencies import dp
# Do not delete (used to register handlers via decorators)
from src.bot import handlers


if __name__ == '__main__':
    """Bot entry point"""
    logger = logging.getLogger(__name__)
    logger.info("Start quiz-bot!")
    executor.start_polling(dp, skip_updates=False)
