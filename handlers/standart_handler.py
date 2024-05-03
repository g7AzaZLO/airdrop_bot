from aiogram import types, Router
from aiogram.filters import CommandStart
from settings.static_messages import WELCOME_MESSAGE

router = Router()


@router.message(CommandStart())
async def start(message: types.Message) -> None:
    print("Processing /start command...")
    await message.answer(text=WELCOME_MESSAGE)
