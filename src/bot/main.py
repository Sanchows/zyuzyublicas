import asyncio
import logging

from aiogram import Bot, Dispatcher, F, filters, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot import handlers
from bot.filters import NoStateFilter
from bot.states import FileGetting
from settings import config
from settings.logger import configure_logging


async def setup_commands(bot: Bot):
    await bot.set_my_commands([
        types.BotCommand(command="start", description="🤝 Приветствие"),
    ])


async def on_startup(*args, **kwargs):
    await setup_commands(bot=kwargs['bot'])


async def on_shutdown(*args, **kwargs):
    await kwargs['dispatcher'].storage.close()


async def main():
    logger.debug("Создаем storage")
    storage = RedisStorage.from_url(url=f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}')
    logger.info("Storage успешно создан, %r", storage)

    dp = Dispatcher(storage=storage)
    logger.debug("Инициализиурем объект бота")
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logger.info("Объект бота успешно создан, %r", bot)

    # setting middlewares
    logger.debug("Регистрируем middlewares")
    logger.info("middlewares успешно зарегистрированы")

    # setting message handlers
    logger.debug("Регистрируем обработчики message")
    dp.message.register(
        handlers.sites_file_processing, FileGetting.sites_file_choosing, F.document,
    )
    logger.info("Обработчики message успешно зарегистрированы")

    # setting callback query handlers
    logger.debug("Регистрируем обработчики message")
    dp.callback_query.register(handlers.btn_load_file_sites, F.data == 'btn_load_file_sites', NoStateFilter())
    dp.callback_query.register(handlers.btn_parse_table_sites, F.data == 'btn_parse_table_sites', NoStateFilter())
    logger.info("Обработчики message успешно зарегистрированы")

    # setting commands
    logger.debug("Регистрируем обработчики комманд")
    dp.message.register(handlers.start, filters.CommandStart(), NoStateFilter())
    logger.info("Обработчики команд успешно зарегистрированы")

    dp.shutdown.register(on_shutdown)
    dp.startup.register(on_startup)

    logger.debug("Запускаем polling")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    configure_logging()
    logger = logging.getLogger('__name__')
    asyncio.run(main())
