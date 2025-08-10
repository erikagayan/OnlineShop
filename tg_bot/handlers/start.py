from aiogram import Router, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

router = Router()


async def _get_user_by_token(token: str) -> tuple:
    """Helper function to fetch user from token."""
    from users.models import User, TelegramToken

    try:
        telegram_token = await sync_to_async(TelegramToken.objects.get)(token=token)
        user = await sync_to_async(lambda: telegram_token.user)()
        return user, telegram_token
    except ObjectDoesNotExist:
        return None, None


async def _check_existing_connection(chat_id: str, user_id: int) -> bool:
    """Check if chat_id is already connected to another user."""
    from users.models import User
    existing_user = await sync_to_async(
        User.objects.filter(telegram_chat_id=chat_id).exclude(id=user_id).first
    )()
    return bool(existing_user)


async def _connect_user_to_telegram(user, chat_id: str, telegram_token) -> None:
    """Connect user to Telegram and clean up."""
    user.telegram_chat_id = chat_id
    await sync_to_async(user.save)()
    await sync_to_async(telegram_token.delete)()


@router.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    """Handle /start command to connect Telegram account."""
    args = message.text.split()

    if len(args) <= 1:
        await message.answer("Hi! Use the link from the app to connect your account.")
        return

    token = args[1]
    chat_id = str(message.chat.id)

    user, telegram_token = await _get_user_by_token(token)
    if not user:
        await message.answer("Invalid or expired token. Please try again.")
        return

    if await _check_existing_connection(chat_id, user.id):
        await message.answer(
            "This Telegram account is already connected to another account. "
            "One Telegram account can only be linked to one user."
        )
        await sync_to_async(telegram_token.delete)()
        return

    await _connect_user_to_telegram(user, chat_id, telegram_token)
    await message.answer("You have successfully connected Telegram to your account!")