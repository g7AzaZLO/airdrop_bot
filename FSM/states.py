from aiogram.fsm.state import StatesGroup, State


class CaptchaState(StatesGroup):
    wait_captcha_state = State()


class RegestrationState(StatesGroup):
    captcha_state = State()
    lang_choose_state = State()
    lang_choose_state_again = State()  # changing the language second time
    hello_state = State()
    proceed_state = State()
    follow_telegram_state = State()
    follow_twitter_state = State()
    submit_address_state = State()
    end_conversation_state = State()
    loop_state = State()
    
    main_menu_state = State()  # State for the main menu