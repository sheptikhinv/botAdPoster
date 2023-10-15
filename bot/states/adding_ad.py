from aiogram.fsm.state import StatesGroup, State


class AddingAd(StatesGroup):
    setting_topic = State()
    entering_title = State()
    entering_description = State()
    adding_photo = State()