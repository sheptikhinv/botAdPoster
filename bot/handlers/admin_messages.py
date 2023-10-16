from aiogram import Router, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.filters import DoesAdminExist, IsAdmin
from bot.keyboards import get_all_admins_markup, get_blocked_users_buttons
from bot.states import AdDecline
from config import get_main_chat_id
from database import User, Topic, Ad

router = Router(name="admin_messages")


@router.message(~DoesAdminExist(), F.text.lower() == "банан", F.chat.type == "private")
async def set_owner(message: Message):
    user = User.get_from_database_by_id(message.from_user.id)
    user.set_role("admin")
    await message.answer("Вы стали главным администратором!")


@router.message(IsAdmin(), Command("admin"), F.chat.type == "private")
async def add_moderator(message: Message, command: CommandObject):
    if not User.is_admin(message.from_user.id):
        await message.answer("У вас нет права назначать новых администраторов!")
        return
    if command.args is None:
        await message.answer("Отправьте /admin @username пользователя, чтоб сделать его админом")
    else:
        user = User.get_from_database_by_username(command.args.replace("@", ""))
        if user is not None:
            try:
                user.set_role("moderator")
                await message.answer(f"Пользователь {user.first_name} сделан администратором!")
                await message.bot.send_message(user.user_id,
                                               f"{message.from_user.username} сделал вас администратором!")
            except Exception as error:
                await message.answer(f"Неожиданная ошибка!\n{error}")
        else:
            await message.answer("Данного пользователя нет в базе данных!")


@router.message(IsAdmin(), Command("blocked"), F.chat.type == "private")
async def get_blocked_users(message: Message):
    reply_markup = get_blocked_users_buttons()
    await message.answer(
        text="Вот список заблокированных пользователей\nДля разблокировки нажмите на кнопку пользователя",
        reply_markup=reply_markup)


@router.message(IsAdmin(), Command("admins"), F.chat.type == "private")
async def get_all_admins(message: Message):
    reply_markup = get_all_admins_markup()
    await message.answer("Вот список всех админов: ", reply_markup=reply_markup)


@router.message(IsAdmin(), Command("newcategory"), F.chat.type == "private")
async def create_new_category(message: Message, command: CommandObject):
    topic_name = command.args
    try:
        topic = await message.bot.create_forum_topic(get_main_chat_id(), topic_name)
        topic_obj = Topic(topic.message_thread_id, topic.name, message.from_user.id)
        topic_obj.add_to_database()
        await message.answer(f"Тема {topic_name} успешно создана!")

    except Exception as error:
        print(error)
        await message.answer(f"Возникла непредвиденная ошибка!\n{error}")


@router.message(IsAdmin(), AdDecline.set_decline_reason)
async def send_decline_reason(message: Message, state: FSMContext):
    ad_id = (await state.get_data())["ad_id"]
    ad = Ad.get_ad_by_id(ad_id)
    await message.answer("Уведомление отправлено пользователю")
    await message.bot.send_message(chat_id=ad.created_by,
                                   text=f"Ваше объявление {ad.title} отклонено по причине:\n{message.text}")
    await state.clear()


def register_admin_messages_handlers(dp: Dispatcher):
    dp.include_router(router)
