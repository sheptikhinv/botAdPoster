from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import User, Topic, Ad


def get_all_admins_markup():
    admin_ids = User.get_all_admins_ids()
    admin_buttons = []
    for user_id in admin_ids:
        user = User.get_from_database_by_id(user_id)
        admin_buttons.append([InlineKeyboardButton(
            text=f"{user.username} - {user.role}",
            callback_data=f"admin get {user.user_id}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=admin_buttons)


def get_admin_markup(user_id: int):
    user = User.get_from_database_by_id(user_id)
    promote_button = InlineKeyboardButton(
        text="⬆️ Передать права гл. админа",
        callback_data=f"admin promote {user.user_id}"
    )
    demote_button = InlineKeyboardButton(
        text="⬇️ Забрать права админа",
        callback_data=f"admin demote {user.user_id}"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[promote_button], [demote_button]])


def get_all_topics_markup():
    topics = Topic.get_all_topics()
    topic_buttons = []
    for topic in topics:
        topic_buttons.append([InlineKeyboardButton(
            text=topic.title,
            callback_data=f"topic set {topic.topic_id}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=topic_buttons)


def get_ad_user_buttons(ad_id: str):
    approve_button = InlineKeyboardButton(
        text="✅",
        callback_data=f"ad moderate {ad_id}"
    )
    cancel_button = InlineKeyboardButton(
        text="❌",
        callback_data=f"ad cancel {ad_id}"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[approve_button, cancel_button]])


def get_ad_admin_buttons(ad: Ad):
    approve_button = InlineKeyboardButton(
        text="✅",
        callback_data=f"ad approve {ad.ad_id}"
    )
    decline_button = InlineKeyboardButton(
        text="❌",
        callback_data=f"ad decline {ad.ad_id}"
    )
    block_button = InlineKeyboardButton(
        text="Заблокировать пользователя",
        callback_data=f"user block {ad.created_by} {ad.ad_id}"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[approve_button, decline_button], [block_button]])


def get_start_button(username):
    start_button = InlineKeyboardButton(
        text="Создать объявление",
        url=f"t.me/{username}?start=123"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[start_button]])


def get_chat_button(chat_invite: str):
    chat_button = InlineKeyboardButton(
        text="Присоединиться к чату",
        url=chat_invite
    )
    return InlineKeyboardMarkup(inline_keyboard=[[chat_button]])


def get_skip_photo_button():
    skip_button = InlineKeyboardButton(
        text="Не добавлять фото",
        callback_data="skip photo"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[skip_button]])
