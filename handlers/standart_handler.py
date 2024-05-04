from aiogram import types, Router
from aiogram.filters import CommandStart
from messages.eng.basic_messages import CAPTCHA_MESSAGE
from logic.captcha import generate_captcha, check_captcha
from aiogram.fsm.context import FSMContext
from FSM.states import CaptchaState

standart_handler_router = Router()


# Handler под команду /start
@standart_handler_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    print("Processing /start command...")
    await generate_captcha(message)
    await state.set_state(CaptchaState.wait_captcha_state)
    await message.answer(text=CAPTCHA_MESSAGE["ENG"])


# Handler состояния капчи
@standart_handler_router.message(CaptchaState.wait_captcha_state)
async def captcha_response_handler(message: types.Message, state: FSMContext) -> None:
    user_response = message.text
    await state.update_data(user_captcha_response=user_response)
    user_answer = await state.get_data()
    result = await check_captcha(message, user_answer)
    if result:
        await state.clear()
