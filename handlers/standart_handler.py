from aiogram import types, Router
from aiogram.filters import CommandStart
from messages.basic_messages import messages
from logic.captcha import generate_captcha, check_captcha
from aiogram.fsm.context import FSMContext
from FSM.states import CaptchaState

standard_handler_router = Router()


def get_message(messages, message_key, language, **kwargs):
	"""
	Retrieve a message based on the key and language,
	formatting it with any provided keyword arguments.
	examples:
		capture_message = get_message(messages, "WELCOME_MESSAGE", "ENG")
		print(capture_message)
		capture_message = get_message(messages, "WELCOME_MESSAGE", "RU", user_name='дурачок')
		print(capture_message)
	"""
	# Retrieve the default values and specific message template
	defaults = messages.get("default_values", {})
	message_template = messages.get(message_key, {}).get(language)
	
	# If the message template exists, use it; otherwise, return a fallback message
	if message_template:
		# Update the default values dictionary with any keyword arguments provided
		all_kwargs = {**defaults, **kwargs}
		return message_template.format(**all_kwargs)
	else:
		return "Message not available."


# Handler под команду /start
@standard_handler_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
	print("Processing /start command...")
	await generate_captcha(message)
	await state.set_state(CaptchaState.wait_captcha_state)
	capture_message = get_message(messages, "WELCOME_MESSAGE", "ENG")
	await message.answer(text=capture_message)


# Handler состояния капчи
@standard_handler_router.message(CaptchaState.wait_captcha_state)
async def captcha_response_handler(message: types.Message, state: FSMContext) -> None:
	user_response = message.text
	await state.update_data(user_captcha_response=user_response)
	user_answer = await state.get_data()
	result = await check_captcha(message, user_answer)
	if result:
		await state.clear()
