from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import types, Router
from keyboards.menu_kb import *

standard_handler_router = Router()


def register_buttons_handlers(dispatcher: Dispatcher, router=standard_handler_router):
	dispatcher.include_router(router)

@standard_handler_router.message(Command(commands=["Menu", "menu", "Меню", "меню"]))
async def show_english_menu(message: types.Message):
	await message.answer("Here is what we have for you:", reply_markup=menu_kb_eng)
