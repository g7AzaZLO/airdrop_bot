from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import types, Router
from keyboards.menu_kb import *

standard_handler_router = Router()

async def start_command(message: types.Message):
    # Send a greeting message with the Russian keyboard
    await message.answer("Выберите опцию:", reply_markup=menu_kb_ru)

# Assuming you have a function to handle the English version
async def show_english_menu(message: types.Message):
    # Send the menu in English
    await message.answer("Select an option:", reply_markup=menu_kb_eng)


def register_buttons_handlers(dispatcher: Dispatcher, router=standard_handler_router):
	dispatcher.include_router(router)

# @standard_handler_router.message(Command(commands=["start"]))
# async def start_command(message: types.Message):
# 	await message.answer("Выберите опцию:", reply_markup=menu_kb_ru)

@standard_handler_router.message(Command(commands=["Профиль", "Profile"]))
async def handle_profile(message: types.Message):
	await message.answer("Here is your profile information...", reply_markup=menu_kb_en)
