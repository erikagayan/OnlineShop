from aiogram import Router
from tg_bot.handlers.start import router as start_router

router = Router()

router.include_router(start_router)

__all__ = ["router"]
