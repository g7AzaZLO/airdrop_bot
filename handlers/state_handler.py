from aiogram import types, Router
from FSM.states import CaptchaState, RegestrationState
from logic.captcha import generate_captcha, check_captcha
from aiogram.fsm.context import FSMContext
from handlers.standart_handler import get_message
from messages.basic_messages import messages

state_handler_router = Router()


# Handler состояния капчи в CaptchaState
@state_handler_router.message(CaptchaState.wait_captcha_state)
async def captcha_response_handler(message: types.Message, state: FSMContext) -> None:
    user_response = message.text
    await state.update_data(user_captcha_response=user_response)
    result = await check_captcha(message)
    if result:
        await state.clear()
        # await state.main_menu


# Handler состояния капчи в регистрации пользователя
@state_handler_router.message(RegestrationState.captcha_state)
async def captcha_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    user_response = message.text
    await state.update_data(user_captcha_response=user_response)
    result = await check_captcha(message)
    if result:
        await state.set_state(RegestrationState.hello_state)
        capture_message = get_message(messages, "WELCOME_MESSAGE", "ENG", user_name=message.from_user.first_name)
        await message.answer(text=capture_message)


@state_handler_router.message(RegestrationState.hello_state)
async def hello_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    user_response = message.text
    await state.update_data(user_hello_response=user_response)
    if user_response == "🚀 Join Airdrop" or "🚀 Присоединиться к аирдропу":
        await state.set_state(RegestrationState.hello_state)
