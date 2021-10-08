import asyncio
import json
import websockets
import time

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from states import StopTracking

from loader import dp
from utils.misc import rate_limit
from keyboards.inline.stop_notification import stop_keyboard


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("set"))
async def tracking_crypto(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if int(user_id) in [609200395]:
        command_args = message.get_args().split()
        print(command_args)
        args_quantity = len(command_args)

        if args_quantity == 0:
            await message.answer('Введите данные!\n'
                                 'Шаблон: /set [Crypt] [Minimum] [Maximum (Optional)]\n'
                                 'Пример: /set btc 45000 [60000]')

        if args_quantity == 1:
            await message.answer('Введите данные!\n'
                                 'Шаблон: /set [Crypt] [Minimum] [Maximum (Optional)]\n'
                                 'Пример: /set btc 45000 [60000]')

        if args_quantity == 2:
            url = f"wss://stream.binance.com:9443/stream?streams={command_args[0]}usdt@miniTicker"

            if command_args[1] == 'stop':
                with open("data.json", 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())

                if command_args[0] in data["user"][f"{user_id}"]["tracking"]:
                    data["user"][f"{user_id}"]["tracking"][command_args[0]] = False

                    json_data = json.dumps(data, indent=4, ensure_ascii=False)
                    with open("data.json", "w", encoding='utf-8') as file:
                        file.write(json_data)

                    await message.answer("Трекинг остановлен!")
                else:
                    await message.answer("Нету данной криптовалюты на трекинге!")

            else:
                min_value = int(command_args[1])

                with open("data.json", 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())

                data["user"][f"{user_id}"]["tracking"][command_args[0]] = True

                json_data = json.dumps(data, indent=4, ensure_ascii=False)
                with open("data.json", "w", encoding='utf-8') as file:
                    file.write(json_data)

                await message.answer('Значение установлено:\n'
                                     f'Min: {min_value}')

                async with websockets.connect(url) as client:
                    while True:
                        with open("data.json", 'r', encoding='utf-8') as f:
                            data = json.loads(f.read())

                        if not data["user"][f"{user_id}"]["tracking"][command_args[0]]:
                            break

                        data = json.loads(await client.recv())['data']

                        event_time = time.localtime(data['E'] // 1000)
                        event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"

                        print(int(float(data['c'])))
                        if int(float(data['c'])) < min_value:
                            while True:
                                with open("data.json", 'r', encoding='utf-8') as f:
                                    data = json.loads(f.read())

                                if data["user"][f"{user_id}"]["tracking"][command_args[0]]:
                                    await message.answer(f"{command_args[0]} ALERT!", reply_markup=stop_keyboard)

                                    await StopTracking.SetStopTracking.set()
                                    await state.update_data(crypt=command_args[0])
                                    await asyncio.sleep(5)
                                else:
                                    await message.answer("Alert stopped!")
                                    break

        elif args_quantity == 3:
            url = f"wss://stream.binance.com:9443/stream?streams={command_args[0]}usdt@miniTicker"
            print(command_args[0])
            print(type(command_args[0]))
            min_value = int(command_args[1])
            max_value = int(command_args[2])

            with open("data.json", 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            data["user"][f"{user_id}"]["tracking"][command_args[0]] = True

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

                    if not data["user"][f"{user_id}"]["tracking"][command_args[0]]:
                        break

                    data = json.loads(await client.recv())['data']

                    event_time = time.localtime(data['E'] // 1000)
                    event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"

                    print(int(float(data['c'])))
                    if int(float(data['c'])) < min_value or int(float(data['c'])) > max_value:
                        while True:
                            with open("data.json", 'r', encoding='utf-8') as f:
                                data = json.loads(f.read())

                            if data["user"][f"{user_id}"]["tracking"][command_args[0]]:
                                await message.answer(f"{command_args[0]} ALERT!", reply_markup=stop_keyboard)

                                await StopTracking.SetStopTracking.set()
                                await state.update_data(crypt=command_args[0])
                                await asyncio.sleep(5)


                                # await state.update_data(crypt=command_args[0])
                            else:
                                await message.answer("Stopped")
                                break
    else:
        await message.answer("Доступ запрещен!\nОбращаться к @Sasha_Zuev\n\n"
                             "Access is denied!\nContact: @Sasha_Zuev")
    # url = f"wss://stream.binance.com:9443/stream?streams={command_args[0]}usdt@miniTicker"
    #
    # if command_args[0] == 'stop':
    #     with open("data.json", 'r', encoding='utf-8') as f:
    #         data = json.loads(f.read())
    #
    #     data["user"][f"{user_id}"]["tracking"] = False
    #
    #     json_data = json.dumps(data, indent=4, ensure_ascii=False)
    #     with open("data.json", "w", encoding='utf-8') as file:
    #         file.write(json_data)
    #
    #     await message.answer("Трекинг остановлен!")
    #
    # else:
    #     min_value = int(command_args.split()[0])
    #     max_value = int(command_args.split()[1])
    #
    #     with open("data.json", 'r', encoding='utf-8') as f:
    #         data = json.loads(f.read())
    #
    #     data["user"][f"{user_id}"]["tracking"] = True
    #
    #     json_data = json.dumps(data, indent=4, ensure_ascii=False)
    #     with open("data.json", "w", encoding='utf-8') as file:
    #         file.write(json_data)
    #
    #     await message.answer('Значения установлены:\n'
    #                          f'Min: {min_value}\n'
    #                          f'Max: {max_value}')
    #
    #     async with websockets.connect(url) as client:
    #         while True:
    #             with open("data.json", 'r', encoding='utf-8') as f:
    #                 data = json.loads(f.read())
    #
    #             if not data["user"][f"{user_id}"]["tracking"]:
    #                 break
    #
    #             data = json.loads(await client.recv())['data']
    #
    #             event_time = time.localtime(data['E'] // 1000)
    #             event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"
    #
    #             print(int(float(data['c'])))
    #             if int(float(data['c'])) < min_value or int(float(data['c'])) > max_value:
    #                 while True:
    #                     with open("data.json", 'r', encoding='utf-8') as f:
    #                         data = json.loads(f.read())
    #
    #                     if data["user"][f"{user_id}"]["tracking"]:
    #                         await message.answer("Btc Command", reply_markup=stop_keyboard)
    #                         await asyncio.sleep(5)
    #                     else:
    #                         await message.answer("Stopped")
    #                         break
