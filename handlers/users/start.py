from aiogram.dispatcher.filters import Command
from aiogram.types import Message
import json
from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("start"))
async def start(message: Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_id = message.from_user.id
    username = message.from_user.username

    with open("data.json", 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    if str(user_id) in data["user"]:
        await message.answer(f"И снова Здравствуйте, {first_name}!")
    else:
        data["user"][f"{user_id}"] = {}
        data["user"][f"{user_id}"]["username"] = username
        data["user"][f"{user_id}"]["first_name"] = first_name
        data["user"][f"{user_id}"]["second_name"] = last_name
        data["user"][f"{user_id}"]["tracking"] = False    # The value of tracking in action. Default - False!

        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        with open("data.json", "w", encoding='utf-8') as file:
            file.write(json_data)

        await message.answer(f'Добро пожаловать, {first_name}')