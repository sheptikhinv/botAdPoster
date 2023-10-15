from aiogram.fsm.state import StatesGroup, State


class AdDecline(StatesGroup):
    set_decline_reason = State()
