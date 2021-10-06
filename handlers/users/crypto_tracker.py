from aiogram.dispatcher.filters import Command
from aiogram.types import Message
import asyncio
from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("btc"))
async def tracking_crypto(message: Message):
    while True:
        await message.answer("Btc Command")
        await asyncio.sleep(5)