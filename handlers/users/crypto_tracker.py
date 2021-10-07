import asyncio
import json
import websockets
import time

from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from utils.misc import rate_limit
from keyboards.inline.stop_notification import stop_keyboard


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("btc"))
async def tracking_crypto(message: Message):
    url = "wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker"
    user_id = message.from_user.id
    command = message.get_full_command()
    command_args = command[1]
    if command_args == 'stop':
        with open("data.json", 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        data["user"][f"{user_id}"]["tracking"] = False

        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        with open("data.json", "w", encoding='utf-8') as file:
            file.write(json_data)

        await message.answer("Трекинг остановлен!")
    else:
        min_value = int(command_args.split()[0])
        max_value = int(command_args.split()[1])

        with open("data.json", 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        data["user"][f"{user_id}"]["tracking"] = True

        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        with open("data.json", "w", encoding='utf-8') as file:
            file.write(json_data)

        await message.answer('Значения установлены:\n'
                             f'Min: {min_value}\n'
                             f'Max: {max_value}')

        async with websockets.connect(url) as client:
            while True:
                with open("data.json", 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())

                if not data["user"][f"{user_id}"]["tracking"]:
                    break

                data = json.loads(await client.recv())['data']

                event_time = time.localtime(data['E'] // 1000)
                event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"

                print(int(float(data['c'])))
                if int(float(data['c'])) < min_value or int(float(data['c'])) > max_value:
                    while True:
                        with open("data.json", 'r', encoding='utf-8') as f:
                            data = json.loads(f.read())

                        if data["user"][f"{user_id}"]["tracking"]:
                            await message.answer("Btc Command", reply_markup=stop_keyboard)
                            await asyncio.sleep(5)
                        else:
                            await message.answer("Stopped")
                            break

