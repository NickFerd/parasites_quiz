"""App config
"""
import logging

from pydantic import BaseSettings
from pathlib import Path

logger = logging.getLogger(__name__)
logger.info(f"{Path.cwd()}")


class Config(BaseSettings):
    bot_token: str
    assets_path: Path = Path('./assets/')  # adapted for docker
    logs_path: Path = Path('./logs')  # adapted for docker
    control_chat_id: int = -734044255
