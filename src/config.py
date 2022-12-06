"""App config
"""

from pydantic import BaseSettings


class Config(BaseSettings):
    bot_token: str
    results_path: str = 'results.json'
