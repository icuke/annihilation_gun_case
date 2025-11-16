from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="start")


@router.message(F.text, CommandStart())
async def cmd_start(message: Message):
    await message.reply("Приветствую! Загрузите документы для обработки")