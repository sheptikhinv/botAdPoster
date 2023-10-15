import asyncio

from bot import start_bot
from config import get_token, check_main_chat_id
from database import create_tables

if __name__ == "__main__":
    token = get_token()
    is_service_mode = not check_main_chat_id()
    create_tables()
    asyncio.run(start_bot(token, is_service_mode))