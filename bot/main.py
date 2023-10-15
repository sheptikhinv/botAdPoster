from aiogram import Bot, Dispatcher

from bot.handlers import register_service_handlers, register_admin_messages_handlers, register_user_handlers, \
    register_admin_callback_handlers

dp = Dispatcher()


def register_handlers():
    register_admin_messages_handlers(dp)
    register_user_handlers(dp)
    register_admin_callback_handlers(dp)


def register_service_mode_handlers():
    register_service_handlers(dp)


async def start_bot(token: str, service_mode: bool):
    bot = Bot(token)
    if service_mode:
        print("Главный чат не задан, бот запускается в сервисном режиме.")
        register_service_mode_handlers()
    else:
        print("Запускаем бота в стандартном режиме...")
        register_handlers()
    await dp.start_polling(bot)
