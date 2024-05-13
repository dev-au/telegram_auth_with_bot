from datetime import timedelta
from secrets import token_hex

from aioredis import Redis
from fastapi import Request, HTTPException

from config import templates
from models import User
from setup import webauth_router


@webauth_router.get('/')
async def home_page(request: Request):
    user_token = request.cookies.get('user_token', None)
    user = await User.get_or_none(token=user_token)
    if user:
        return templates.TemplateResponse(request, 'success.html')
    host = str(request.client.host)
    return templates.TemplateResponse(request, 'home.html', {'host': host})


@webauth_router.get('/enter/{token}')
async def register_with_bot(request: Request, token: str):
    redis: Redis = request.app.redis
    redis_user = await redis.get(token)
    if not redis_user:
        raise HTTPException(status_code=502, detail='Bad Gateway with your token')
    else:
        redis_user = redis_user.decode('utf-8')
        telegram_id = int(redis_user.split(':')[0])
        phone = redis_user.split(':')[1]
        cookie_token = token_hex()
        user_exists = await User.get_or_none(telegram_id=telegram_id)
        if user_exists:
            user_exists.token = cookie_token
            await user_exists.save()
        else:
            await User.create(telegram_id=telegram_id, phone=phone, token=cookie_token)
        await redis.delete(token)
        response = templates.TemplateResponse(request, 'success.html')
        response.set_cookie('user_token', cookie_token)
        return response


@webauth_router.get('/generate-token/{token}/{data}/{secret_key}')
async def generate_token(request: Request, token: str, data: str, secret_key: str):
    redis: Redis = request.app.redis
    if secret_key == 'secret_key':
        await redis.setex(token, timedelta(minutes=10), data)
        return {'success': True}
    else:
        raise HTTPException(400)
