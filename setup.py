from aiogram.dispatcher.dispatcher import Bot, Dispatcher
from fastapi import APIRouter

from config import *

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

webauth_router = APIRouter(prefix='')
