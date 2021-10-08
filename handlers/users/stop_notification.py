import asyncio
import json

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_data import stop_notification_callback
from loader import dp
from utils.misc import rate_limit
from keyboards.inline.stop_notification import stop_keyboard
from aiogram.dispatcher import FSMContext
from states import StopTracking


@dp.callback_query_handler(stop_notification_callback.filter(crypt='btc'), state=StopTracking.SetStopTracking)
async def stop_alert(call: CallbackQuery, state: FSMContext):
    """Stop tracking"""
    await call.answer(text='Трекинг осановлен!', cache_time=5)
    user_id = call.from_user.id

    if int(user_id) in [609200395]:
        data = await state.get_data()
        crypt_name = data.get("crypt")

        with open("data.json", 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        data["user"][f"{user_id}"]["tracking"][crypt_name] = False

        json_data = json.dumps(data, indent=4, ensure_ascii=False)

        with open("data.json", "w", encoding='utf-8') as file:
            file.write(json_data)

        await call.message.answer(f"{crypt_name} трекинг остановлен!")
        await state.finish()
    else:
        await call.message.answer("Доступ запрещен!\nОбращаться к @Sasha_Zuev\n\n"
                                  "Access is denied!\nContact: @Sasha_Zuev")


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("stopAll"))
async def stop_all_trackers(message: Message):

    user_id = message.from_user.id

    if int(user_id) in [609200395]:
        with open("data.json", 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        for x in data["user"][f"{user_id}"]["tracking"]:
            print(x)
            data["user"][f"{user_id}"]["tracking"][x] = False

        json_data = json.dumps(data, indent=4, ensure_ascii=False)

        with open("data.json", "w", encoding='utf-8') as file:
            file.write(json_data)

        await message.answer("Все трекинги остановлены!")
    else:
        await message.answer("Доступ запрещен!\nОбращаться к @Sasha_Zuev\n\n"
                             "Access is denied!\nContact: @Sasha_Zuev")


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("stop"))
async def stop_selected_tracker(message: Message):
    user_id = message.from_user.id

    if int(user_id) in [609200395]:
        command_args = message.get_args().split()
        print(command_args)
        args_quantity = len(command_args)

        with open("data.json", 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        data["user"][f"{user_id}"]["tracking"][command_args[0]] = False
        json_data = json.dumps(data, indent=4, ensure_ascii=False)

        with open("data.json", "w", encoding='utf-8') as file:
            file.write(json_data)

        await message.answer(f"{command_args[0]} трекинг остановлен")
    else:
        await message.answer("Доступ запрещен!\nОбращаться к @Sasha_Zuev\n\n"
                             "Access is denied!\nContact: @Sasha_Zuev")
