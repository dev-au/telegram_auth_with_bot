from aiogram.types import Update, BotCommand
from aioredis import from_url
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import DB_URL, REDIS_URL, WEBHOOK_URL
from setup import dp, bot, webauth_router
import bot_auth, web_auth

app = FastAPI()
app.include_router(webauth_router)


@app.on_event('startup')
async def start_project():
    await bot.set_webhook(url=WEBHOOK_URL + '/webhook')
    await bot.set_my_commands([
        BotCommand(command='/start', description='Create New Token'),
        BotCommand(command='/restart', description='Update New Token'),
    ])
    redis = await from_url(REDIS_URL)
    app.redis = redis
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={'models': ['models']},
        generate_schemas=True
    )


@app.post('/webhook')
async def webhook_bot(update: Update):
    await dp.feed_update(bot, update)
