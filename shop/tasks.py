import asyncio
from aiogram import Bot
from users.models import User
from celery import shared_task
from shop.models import Product
from django.conf import settings


async def send_telegram_notification(bot, chat_id, message):
    """Asynchronous sending of messages in Telegram."""
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Error sending message in Telegram {chat_id}: {e}")


@shared_task
def notify_users_about_inventory_change(product_id, old_inventory, new_inventory):
    """Sending notifications to users about changes in product quantities."""
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

    # Create a new event loop for this task
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Receive the product
        product = Product.objects.get(id=product_id)
        message = (
            f"Product '{product.title}' updated!\n"
            f"Was: {old_inventory} pcs.\n"
            f"Became: {new_inventory} pcs."
        )

        # Getting users from Telegram
        users = User.objects.filter(telegram_chat_id__isnull=False)

        # Forming tasks for sending messages
        tasks = [
            send_telegram_notification(bot, user.telegram_chat_id, message)
            for user in users
        ]

        # We perform all tasks asynchronously
        loop.run_until_complete(asyncio.gather(*tasks))

    except Product.DoesNotExist:
        print(f"Product with ID {product_id} not found")
    except Exception as e:
        print(f"Error in the task notify_users_about_inventory_change: {e}")
    finally:
        # Close the bot session and event loop
        loop.run_until_complete(bot.session.close())
        loop.close()
