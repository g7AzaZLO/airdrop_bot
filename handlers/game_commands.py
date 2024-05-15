from aiogram import types, Router
from aiogram.filters import Command
from messages.game_messages import *
# from aiogram.filters import CommandStart
# from messages.basic_messages import messages
# from logic.captcha import generate_captcha, check_captcha
# from aiogram.fsm.context import FSMContext
# from FSM.states import CaptchaState

import random

standard_handler_router = Router()


def setup_game_routes(dispatcher):
	router = Router()
	router.message.register(roll, Command(commands=['roll']))
	dispatcher.include_router(router)


async def roll(message: types.Message) -> None:
	# Message text includes the command; split to get arguments
	parts = message.text.split()
	# Set default values
	low, high = 1, 100
	
	# Check if user provided any numbers
	if len(parts) == 2:
		try:
			# Only one number provided, set high to this number
			high = int(parts[1])
			if high < 1:
				raise ValueError("Upper bound must be at least 1.")
		except ValueError:
			await message.reply("Please provide a valid number like: /roll 20")
			return
	elif len(parts) >= 3:
		try:
			# Two numbers provided, set low and high accordingly
			low, high = map(int, parts[1:3])
			if low >= high:
				raise ValueError("Lower bound must be less than upper bound.")
		except ValueError:
			await message.reply("Please provide valid lower and upper bounds like: /roll 10 20")
			return
	
	# Generate the random number
	result = random.randint(low, high)
	# Select a random message from the dictionary and format it
	random_key = random.choice(list(messages_roll.keys()))
	response_message = messages_roll[random_key].format(result=result, low=low, high=high)
	# Send the formatted response back to the user
	await message.reply(response_message)
