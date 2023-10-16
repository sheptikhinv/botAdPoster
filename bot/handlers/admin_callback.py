import aiogram.exceptions
from aiogram import Router, Dispatcher, F
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.filters import IsAdmin
from bot.keyboards import get_admin_markup, get_start_button, get_blocked_users_buttons
from bot.misc import user_ad_preview
from bot.states import AdDecline
from config import get_main_chat_id
from database import User, Ad, Topic

router = Router(name="admin_callback")


@router.callback_query(IsAdmin(), F.data.contains("get"))
async def get_admin(callback_query: CallbackQuery):
    admin_id = int(callback_query.data.split()[2])
    user = User.get_from_database_by_id(admin_id)
    reply_markup = None
    if admin_id != callback_query.from_user.id and User.is_admin(callback_query.from_user.id):
        reply_markup = get_admin_markup(admin_id)
    await callback_query.message.answer(text=f"Имя: {user.first_name}\n"
                                             f"Юзернейм: {user.username}\n"
                                             f"Роль: {user.role}\n",
                                        reply_markup=reply_markup)
    await callback_query.answer()


@router.callback_query(IsAdmin(), or_f(F.data.contains("promote"), F.data.contains("demote")))
async def change_admin_status(callback_query: CallbackQuery):
    args = callback_query.data.split()
    action, admin_id = args[1], int(args[2])
    if admin_id == callback_query.from_user.id:
        await callback_query.answer()
        return
    user = User.get_from_database_by_id(admin_id)
    if action == "promote":
        this_user = User.get_from_database_by_id(callback_query.from_user.id)
        user.set_role("admin")
        this_user.set_role("moderator")
        await callback_query.message.answer(
            "Пользователь повышен до главного админа!\nВаш статус понижен до модератора")
    elif action == "demote":
        user.set_role("user")
        await callback_query.message.answer("Администратор понижен до обычного пользователя")

    await callback_query.answer()


@router.callback_query(IsAdmin(), F.data.contains("approve"))
async def approve_ad(callback_query: CallbackQuery):
    args = callback_query.data.split()
    ad = Ad.get_ad_by_id(args[2])
    reply_markup = get_start_button((await callback_query.bot.get_me()).username)
    if ad.status == "checking":
        try:
            if ad.photo_id is not None:
                await callback_query.bot.send_photo(chat_id=get_main_chat_id(),
                                                    message_thread_id=ad.topic_id,
                                                    caption=user_ad_preview(ad.title, ad.description),
                                                    photo=ad.photo_id,
                                                    reply_markup=reply_markup)
            else:
                await callback_query.bot.send_message(chat_id=get_main_chat_id(),
                                                      message_thread_id=ad.topic_id,
                                                      text=user_ad_preview(ad.title, ad.description),
                                                      reply_markup=reply_markup)
            await callback_query.message.answer("Объявление опубликовано")
            ad.change_status("sent")
        except aiogram.exceptions.TelegramBadRequest as error:
            topic = Topic.get_topic_by_id(ad.topic_id)
            topic.delete_from_database()
            await callback_query.message.answer(f"Неожиданная ошибка!\n{error}\nКатегория удалена!")
    else:
        await callback_query.message.answer("Объявление уже было рассмотрено другим админом")
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()


@router.callback_query(IsAdmin(), F.data.contains("decline"))
async def decline_ad(callback_query: CallbackQuery, state: FSMContext):
    args = callback_query.data.split()
    ad = Ad.get_ad_by_id(args[2])
    if ad.status == "checking":
        ad.change_status("declined")
        await state.update_data(ad_id=ad.ad_id)
        await state.set_state(AdDecline.set_decline_reason)
        await callback_query.message.answer("Пользователю отказано в публикации. Напишите причину отказа в следующем сообщении")
    else:
        await callback_query.message.answer("Объявление уже было рассмотрено другим админом")
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()


@router.callback_query(IsAdmin(), F.data.contains("unblock"))
async def unblock_user(callback_query: CallbackQuery):
    args = callback_query.data.split()
    user = User.get_from_database_by_id(int(args[2]))
    if user.role == "blocked":
        user.set_role("user")
        await callback_query.message.answer(f"Пользователь {user.first_name} - @{user.username} разблокирован")
        await callback_query.message.edit_reply_markup(reply_markup=get_blocked_users_buttons())
    await callback_query.answer()


@router.callback_query(IsAdmin(), F.data.contains("block"))
async def block_user(callback_query: CallbackQuery):
    args = callback_query.data.split()
    user = User.get_from_database_by_id(int(args[2]))
    ad = Ad.get_ad_by_id(args[3])
    if ad.status == "checking":
        user.set_role("blocked")
        ad.change_status("declined")
        await callback_query.message.answer(f"Пользователь {user.first_name} - @{user.username} заблокирован")
    else:
        await callback_query.message.answer("Объявление уже было рассмотрено другим админом")
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()


def register_admin_callback_handlers(dp: Dispatcher):
    dp.include_router(router)
