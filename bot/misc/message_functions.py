import asyncio

from aiogram.types import CallbackQuery

from bot.keyboards import get_ad_admin_buttons
from bot.misc import admin_ad_preview
from database import Ad, User


async def send_ad_to_admins(ad: Ad, callback_query: CallbackQuery):
    user = User.get_from_database_by_id(ad.created_by)
    text = admin_ad_preview(ad, user)
    reply_markup = get_ad_admin_buttons(ad)
    for user_id in User.get_all_admins_ids():
        if ad.photo_id is not None:
            await callback_query.bot.send_photo(chat_id=user_id, caption=text, photo=ad.photo_id, reply_markup=reply_markup)
        else:
            await callback_query.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
        await asyncio.sleep(0.3)
