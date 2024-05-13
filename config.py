from fastapi.templating import Jinja2Templates

DB_URL = 'sqlite://db.sqlite3'
REDIS_URL = 'redis://localhost:6379/2'

BOT_TOKEN = '635268134:AAHf-18NvOBzV1SJRo0GloPzHtHUrQBFOA'
WEBHOOK_URL = 'https://your-url.ngrok-free.app'

templates = Jinja2Templates(directory='templates')
