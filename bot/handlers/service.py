from aiogram import Router, F, Dispatcher
from aiogram.types import ChatMemberUpdated
from aiogram.types.chat import Chat

from config import set_main_chat_id, check_main_chat_id

router = Router(name="service")


@router.my_chat_member(F.chat.type == "supergroup", F.new_chat_member.status == "member")
async def get_main_chat_handler(update: ChatMemberUpdated):
    if check_main_chat_id(): return
    if update.chat.is_forum:
        set_main_chat_id(str(update.chat.id))
        print(f"Чат {update.chat.title} установлен! Перезапустите бота для работы в стандартном режиме.")
    else:
        print(f"В чате {update.chat.title} отключены темы. Включите и пригласите бота снова!")


def register_service_handlers(dp: Dispatcher):
    dp.include_router(router)
