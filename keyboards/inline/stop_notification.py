from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import stop_notification_callback

stop_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Остановить оповещение!",
                                 callback_data=stop_notification_callback.new(
                                     crypt="btc"))
        ]
    ]
)