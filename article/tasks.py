import os
import asyncio
import logging
from aiogram import Bot
from .utils import get_subscribers


API_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
bot = Bot(API_TOKEN)


async def send_article_notification(article):
    """Notify subscribers about a new article."""
    subscribers = get_subscribers()
    for user_id in subscribers:
        try:
            await bot.send_message(
                user_id,
                f"New Article Alert!\n\nTitle: {article.title}"
                f"\nContent: {article.content}",
            )
        except Exception as e:
            logging.error(f"Failed to send message to {user_id}: {e}")


def send_article_notification_sync(article):
    """Synchronous wrapper to call async function."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_article_notification(article))
