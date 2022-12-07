"""App config
"""

from pydantic import BaseSettings


class Config(BaseSettings):
    bot_token: str
    results_path: str = 'results.json'
    control_chat_id: int = -734044255
