import asyncio
from tg_bot.bot import bot, dp
from tg_bot.handlers import router


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
