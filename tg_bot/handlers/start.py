from aiogram import Router, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    args = message.text.split()
    if len(args) > 1:
        token = args[1]
        print(f"Processing token: {token}")
        try:
            from users.models import User, TelegramToken
            # Get the TelegramToken object asynchronously
            telegram_token = await sync_to_async(TelegramToken.objects.get)(token=token)
            # Get the associated user asynchronously
            user = await sync_to_async(lambda: telegram_token.user)()
            # Get user email asynchronously (for debugging)
            user_email = await sync_to_async(lambda: user.email)()
            # Set telegram_chat_id and save
            user.telegram_chat_id = str(message.chat.id)
            await sync_to_async(user.save)()
            await sync_to_async(telegram_token.delete)()
            await message.answer("You have successfully connected Telegram to your account!")
        except TelegramToken.DoesNotExist:
            await message.answer("Invalid or expired token. Please try again.")
    else:
        await message.answer("Hi! Use the link from the app to connect your account.")
