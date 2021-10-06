import asyncio
import json

from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from utils.misc import rate_limit
from keyboards.inline.stop_notification import stop_keyboard


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("btc"))
async def tracking_crypto(message: Message):
    user_id = message.from_user.id

    with open("data.json", 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    data["user"][f"{user_id}"]["tracking"] = True

    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    with open("data.json", "w", encoding='utf-8') as file:
        file.write(json_data)

    # TODO: Add condition before cycle
    while True:
        with open("data.json", 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        if data["user"][f"{user_id}"]["tracking"]:
            await message.answer("Btc Command", reply_markup=stop_keyboard)
            await asyncio.sleep(5)
        else:
            await message.answer("Stopped")
            break
