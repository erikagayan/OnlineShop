"""
This file creates and configures the main objects for the Telegram bot to work.
"""

from aiogram import Bot, Dispatcher
from tg_bot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
