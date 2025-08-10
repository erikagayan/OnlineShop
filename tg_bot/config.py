"""
config.py — File for storing project configuration settings.

This file loads environment variables from .env and provides access to:
- BOT_TOKEN — Telegram bot token

The file automatically loads variables from .env if they are defined there.
"""

from pathlib import Path
from decouple import Config, RepositoryEnv

env_path = Path(__file__).resolve().parent.parent / "online_shop" / ".env"
config = Config(RepositoryEnv(env_path))

BOT_TOKEN = config("BOT_TOKEN")
DJANGO_SETTINGS_MODULE = "online_shop.settings"
