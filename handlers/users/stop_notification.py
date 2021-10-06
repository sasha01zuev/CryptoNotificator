import asyncio
import json

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_data import stop_notification_callback
from loader import dp
from utils.misc import rate_limit
from keyboards.inline.stop_notification import stop_keyboard


@dp.callback_query_handler(stop_notification_callback.filter(crypt='btc'))
async def stop_alert(call: CallbackQuery):
    """Change value in data.json and stop cycle of alert"""
    user_id = call.from_user.id

    with open("data.json", 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    data["user"][f"{user_id}"]["tracking"] = False

    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    with open("data.json", "w", encoding='utf-8') as file:
        file.write(json_data)

    await call.answer("Остановлено!", cache_time=5)
    await call.message.delete()
