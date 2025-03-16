from aiogram.types import Message

from bot import constants
from bot.keyboards import keyboard_start


async def send_start_menu_message(message: Message):
    await message.answer(text=constants.MAIN_MENU_MESSAGE, reply_markup=keyboard_start)
