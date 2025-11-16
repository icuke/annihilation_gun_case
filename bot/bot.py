import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import settings
from handlers import get_handlers_router


logging.basicConfig(level=settings.LOGGING_LEVEL)
logger = logging.getLogger("main")

bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


async def on_startup() -> None:
    logger.info("Бот запускается...")

    dp.include_router(get_handlers_router())

    await set_commands()

    bot_info = await bot.get_me()

    states: dict[bool | None, str] = {
        True: "Enabled",
        False: "Disabled",
        None: "Unknown (This's not a bot)",
    }

    logger.info(f"Groups Mode  - {states[bot_info.can_join_groups]}")
    logger.info(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logger.info(f"Inline Mode  - {states[bot_info.supports_inline_queries]}")

    logger.info("Бот запущен")


async def on_shutdown() -> None:
    logger.info("Бот останавливается...")

    await dp.storage.close()
    await dp.fsm.storage.close()

    await bot.delete_webhook()
    await bot.session.close()

    logger.info("Бот остановлен")


async def set_commands():
    commands = [
        BotCommand(command="start", description="Запуск бота"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    # регистрация функций
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
