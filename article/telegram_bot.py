import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv()

bot = Bot(os.environ["TELEGRAM_BOT_TOKEN"])
dp = Dispatcher(bot=bot)

API_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API_ENDPOINT = "http://blog:8000/api/articles/latest-article/"


def get_subscribers():
    user_model = get_user_model()
    return [user.id for user in user_model.objects.all()]


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
    user_id = message.from_user.id
    user = get_user_model().objects.filter(id=user_id).first()
    if user and not user.is_subscribed:
        user.is_subscribed = True
        user.save()
        await message.reply("You have been subscribed to blog updates.")
    else:
        await message.reply("You are already subscribed or not a registered user.")


@dp.message_handler(commands=["unsubscribe"])
async def unsubscribe(message: types.Message):
    """Command handler for '/unsubscribe'."""
    user_id = message.from_user.id
    user = get_user_model().objects.filter(id=user_id).first()
    if user and user.is_subscribed:
        user.is_subscribed = False
        user.save()
        await message.reply("You have been unsubscribed from blog updates.")
    else:
        await message.reply("You are not subscribed or not a registered user.")


if __name__ == "__main__":
    executor.start_polling(dp)
