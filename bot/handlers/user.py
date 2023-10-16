import asyncio

import aiogram.exceptions
from aiogram import Router, F, Dispatcher
from aiogram.filters import Command, CommandObject, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.filters.blocked import IsBlocked
from bot.keyboards import get_all_topics_markup, get_ad_user_buttons, get_ad_admin_buttons, get_chat_button, \
    get_skip_photo_button
from bot.misc import user_ad_preview, id_generator, admin_ad_preview, send_ad_to_admins
from bot.states import AddingAd
from config import get_main_chat_id
from database import User, Ad

router = Router(name="user")


@router.message(IsBlocked(), F.chat.type == "private")
async def blocked_user(message: Message):
    await message.answer("Вы заблокированы.")


@router.message(F.forward_from)
async def ignore_forward(message: Message):
    pass


@router.message(Command("start"), F.chat.type == "private")
async def start_message(message: Message, command: CommandObject, state: FSMContext):
    if User.is_user_new(message.from_user.id):
        user = User(message.from_user.id, message.from_user.first_name, message.from_user.username, "user")
        user.add_to_database()
    if command.args is None:
        await message.answer("Привет! Если хотите создать объявление - пишите /create")
    else:
        await start_new_ad(message, state)


@router.message(Command("create"), F.chat.type == "private")
async def start_new_ad(message: Message, state: FSMContext):
    member = await message.bot.get_chat_member(get_main_chat_id(), message.from_user.id)
    if member.status in ["left", "restricted", "banned"]:
        await message.answer("Сначала подпишитесь на наш чат!", reply_markup=get_chat_button(
            await message.bot.export_chat_invite_link(get_main_chat_id())))
        return
    await message.answer(
        text="Выберите категорию для своего объявления!",
        reply_markup=get_all_topics_markup())
    await state.set_state(AddingAd.setting_topic)


@router.callback_query(F.data.contains("set"), AddingAd.setting_topic)  # Если кто-то будет тут копаться:
async def setting_topic(callback_query: CallbackQuery, state: FSMContext):  # сорян, я подумал лучше этот callback сюда
    await state.update_data(ad_topic=callback_query.data.split()[2])  # впихнуть для наглядности создания объекта
    await callback_query.message.edit_text(text=callback_query.message.text, reply_markup=None)
    await state.set_state(AddingAd.entering_title)
    await callback_query.message.answer("Теперь введите название для вашего объявления")
    await callback_query.answer()


@router.message(AddingAd.entering_title, F.text, F.chat.type == "private")
async def setting_title(message: Message, state: FSMContext):
    await state.update_data(ad_title=message.text)
    await message.answer("Отлично, теперь отправьте полное описание вашего товара.\n\n"
                         "Не забудьте указать свои контакты для связи!")
    await state.set_state(AddingAd.entering_description)


@router.message(AddingAd.entering_description, F.text, F.chat.type == "private")
async def setting_description(message: Message, state: FSMContext):
    await state.update_data(ad_description=message.text)
    await message.answer(
        text="Описание добавлено! Если хотите добавить фотографию, отправьте её сейчас (максимум одну!)\n"
             'Если хотите создать объявление без фотографии, нажмите кнопку "Отправить без фото"',
        reply_markup=get_skip_photo_button())
    await state.set_state(AddingAd.adding_photo)


@router.message(AddingAd.adding_photo, F.photo, F.chat.type == "private")
async def setting_photo(message: Message, state: FSMContext):
    await state.update_data(ad_photo=message.photo[-1].file_id)
    await message.answer("Объявление готово! Проверьте всё в следующем сообщении и сможете отправить его на проверку!")
    await preview_ad(message, state, message.from_user.id)


@router.callback_query(AddingAd.adding_photo, F.data.contains("skip"))
async def not_setting_photo(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(ad_photo=None)
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer("Объявление готово! Проверьте всё в следующем сообщении и сможете отправить его на проверку!")
    await preview_ad(callback_query.message, state, callback_query.from_user.id)


async def preview_ad(message: Message, state: FSMContext, user_id: int):
    ad_data = await state.get_data()
    ad_id = id_generator()
    text = user_ad_preview(ad_data["ad_title"], ad_data["ad_description"])
    ad = Ad(
        title=ad_data["ad_title"],
        description=ad_data["ad_description"],
        photo_id=ad_data["ad_photo"],
        created_by=user_id,
        topic_id=ad_data["ad_topic"],
        ad_id=ad_id,
        status="checking"
    )
    reply_markup = get_ad_user_buttons(ad_id)
    ad.add_to_database()
    await state.clear()
    try:
        if ad.photo_id is not None:
            await message.answer_photo(caption=text, photo=ad.photo_id, reply_markup=reply_markup)
        else:
            await message.answer(text=text, reply_markup=reply_markup)
    except aiogram.exceptions.TelegramBadRequest as error:
        if error.message == "Bad Request: message is too long" or error.message == "Bad Request: message caption is too long":
            await message.answer("Ваше объявление слишком длинное. Сократите описание и попробуйте снова.")


@router.callback_query(F.data.contains("moderate"))
async def send_ad_to_moderation(callback_query: CallbackQuery):
    args = callback_query.data.split()
    ad = Ad.get_ad_by_id(args[2])
    ad.change_status("checking")
    await callback_query.message.edit_reply_markup(reply_markup=None)
    try:
        await send_ad_to_admins(ad, callback_query)
        await callback_query.message.answer("Ваше объявление отправлено на проверку!")
    except aiogram.exceptions.TelegramBadRequest as error:
        if error.message == "Bad Request: message is too long" or error.message == "Bad Request: message caption is too long":
            await callback_query.message.answer("Ваше объявление слишком длинное. Сократите описание и попробуйте снова.")



@router.callback_query(F.data.contains("cancel"))
async def cancel_ad(callback_query: CallbackQuery):
    args = callback_query.data.split()
    ad = Ad.get_ad_by_id(args[2])
    ad.change_status("cancelled")
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer("Объявление удалено")


def register_user_handlers(dp: Dispatcher):
    dp.include_router(router)
