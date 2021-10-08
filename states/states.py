from aiogram.dispatcher.filters.state import StatesGroup, State


# Example:
# class Start(StatesGroup):
#     SetStartCommand = State()

class StopTracking(StatesGroup):
    SetStopTracking = State()
