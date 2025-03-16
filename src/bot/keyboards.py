from aiogram import types

from bot import constants

button_load_file_sites = types.InlineKeyboardButton(
    text=constants.LOAD_FILE_BTN, callback_data='btn_load_file_sites')
button_parse_table_sites = types.InlineKeyboardButton(
    text=constants.PARSE_TABLE_SITES_BTN, callback_data='btn_parse_table_sites')

keyboard_start = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [button_load_file_sites, button_parse_table_sites,]
    ],
)
