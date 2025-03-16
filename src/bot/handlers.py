import logging
from io import BytesIO
from pathlib import Path

from aiogram import types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from bot import constants
from bot.services import load_sites_from_bytes_io
from bot.states import FileGetting
from bot.utils import send_start_menu_message
from files.exceptions import MissedRequiredColumnsException, InvalidFileDataException
from parser.services import get_avg_prices_by_site
from settings import config

logger = logging.getLogger(__name__)


async def start(message: types.Message):
    logger.info("Получили сообщение %r", message.message_id)
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await message.answer(text=constants.START_MESSAGE)
    await send_start_menu_message(message)
    logger.info("Сообщение %r успешно обработано", message.message_id)


async def btn_load_file_sites(callback_query: types.CallbackQuery, state: FSMContext):
    logger.info("Получили callback_query %r , сообщение %r", callback_query.id, callback_query.message.message_id)
    await callback_query.answer()
    await callback_query.bot.send_chat_action(callback_query.message.chat.id, ChatAction.TYPING)
    logger.debug("Устанавливаем 'FileGetting.sites_file_choosing' для сообщения %r", callback_query.message.message_id)
    await state.set_state(FileGetting.sites_file_choosing)
    await callback_query.message.answer(text=constants.LOAD_SITES_EXCEL_FILE_MESSAGE, reply_markup=None)
    logger.info("callback_query %r успешно обработано", callback_query.id)


async def sites_file_processing(message: types.Message, state: FSMContext):
    # TODO: сделать ограничение на максимальный размер файла, чтобы избежать перегруза ОЗУ на сервере
    logger.info("Получили сообщение %r", message.message_id)
    if (ext := Path(message.document.file_name).suffix.lower()) not in config.EXCEL_EXTENSIONS:
        await message.answer(
            text=constants.INVALID_EXCEL_EXTENSIONS_MESSAGE.format(
                ext=ext, allowed_extensions=", ".join(config.EXCEL_EXTENSIONS)),
        )
        return
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    # Качаем файл и записываем в буфер
    logger.debug("Получаем файл %s", message.document.file_id)
    file = await message.bot.get_file(message.document.file_id)
    logger.info("Скачиваем файл %s", file.file_path)
    downloaded_file = await message.bot.download_file(file.file_path)
    logger.debug("Сохраняем файл %s в io.BytesIO", downloaded_file)
    bytes_io = BytesIO(downloaded_file.getvalue())
    try:
        # получаем сайты из полученного файла и загружаем в таблицу
        data_text = await load_sites_from_bytes_io(bytes_io)
    except MissedRequiredColumnsException as e:
        await message.answer(text=e.message)
    except InvalidFileDataException as e:
        await message.answer(text=e.message)
    else:
        if data_text:
            text = constants.AFTER_LOADING_SITES_EXCEL_FILE_MESSAGE.format(data=data_text)
        else:
            text = constants.AFTER_LOADING_SITES_EXCEL_FILE_NO_DATA_MESSAGE
        await state.clear()
        await message.answer(text=text)
        await send_start_menu_message(message)
        logger.info("Сообщение %r успешно обработано", message.message_id)


async def btn_parse_table_sites(callback_query: types.CallbackQuery):
    logger.info("Получили callback_query %r , сообщение %r", callback_query.id, callback_query.message.message_id)
    await callback_query.answer()
    await callback_query.bot.send_chat_action(callback_query.message.chat.id, ChatAction.TYPING)
    await callback_query.message.answer(text="Парсим данные, ожидайте, это занимает некоторое время...")
    await callback_query.bot.send_chat_action(callback_query.message.chat.id, ChatAction.TYPING)
    try:
        avg_prices = await get_avg_prices_by_site()
    except Exception as e:
        await callback_query.message.answer(text="Oops... Что-то пошло не так")
        raise e from None

    avg_prices_text = [
        constants.AVG_PRICE_TEMPLATE.format(site=site, avg_price=avg_price)
        for site, avg_price in avg_prices.items()
    ]
    await callback_query.message.answer(
        text=constants.AFTER_PARSE_TABLE_SITES_MESSAGE.format(avg_prices="\n".join(avg_prices_text)),
        reply_markup=None
    )
    await send_start_menu_message(callback_query.message)
    logger.info("callback_query %r успешно обработано", callback_query.id)
