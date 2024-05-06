from aiogram.fsm.state import StatesGroup, State


class CaptchaState(StatesGroup):
    wait_captcha_state = State()

class RegestrationState(StatesGroup):
    captcha_state = State()
    proceed_state = State()
    follow_telegram_state = State()
    follow_twitter_state = State()
    submit_address_state = State()
    end_conversation_state = State()
    loop_state = State()