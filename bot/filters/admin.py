from aiogram.filters import Filter
from aiogram.types import Message

from database import User


class DoesAdminExist(Filter):
    async def __call__(self, message: Message) -> bool:
        return User.does_admin_exist()


class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in User.get_all_admins_ids()