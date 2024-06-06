import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()

bot = Bot(os.environ["TELEGRAM_BOT_TOKEN"])
dp = Dispatcher(bot=bot)

API_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API_ENDPOINT = "http://blog:8000/api/articles/latest-articles/"

subscribers = []


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    """Command handler for '/start'. Greets an user."""
    await message.answer("Welcome to the Article Blog Bot!")


@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    """Command handler for '/help'. Sends list of available commands."""
    await message.answer(
        "/start - Welcome message\n/help - List of available commands"
        "\n/latest - Get the latest article"
        "\n/subscribe - Subscribe to blog updates"
        "\n/unsubscribe - Unsubscribe from blog updates"
    )


@dp.message_handler(commands=["latest"])
async def get_latest_article(message: types.Message):
    """Command handler for '/latest'. Sends a data about the latest article."""
    async with aiohttp.ClientSession() as session:
        async with session.get(API_ENDPOINT) as response:
            if response.status == 200:
                data = await response.json()
                article = data[0]
                title = article["title"]
                content = article["content"]
                await message.reply(
                    f"Latest Article:\n\nTitle: {title}\nContent: {content}"
                )
            else:
                await message.reply("Failed to retrieve the latest article.")


@dp.message_handler(commands=["subscribe"])
async def subscribe(message: types.Message):
    """Command handler for '/subscribe'."""
    if message.from_user.id not in subscribers:
        subscribers.append(message.from_user.id)
        await message.reply("You have been subscribed to blog updates.")
    else:
        await message.reply("You are already subscribed.")


@dp.message_handler(commands=["unsubscribe"])
async def unsubscribe(message: types.Message):
    """Command handler for '/unsubscribe'."""
    if message.from_user.id in subscribers:
        subscribers.remove(message.from_user.id)
        await message.reply("You have been unsubscribed from blog updates.")
    else:
        await message.reply("You are not subscribed.")


async def notify_subscribers(article):
    """Notify subscribers about a new article."""
    for user_id in subscribers:
        try:
            await bot.send_message(
                user_id,
                f"New Article Alert!\n\nTitle: {article['title']}"
                f"\nContent: {article['content']}",
            )
        except Exception as e:
            logging.error(f"Failed to send message to {user_id}: {e}")


if __name__ == "__main__":
    executor.start_polling(dp)
