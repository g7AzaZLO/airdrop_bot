from aiogram.fsm.state import StatesGroup, State


class CaptchaState(StatesGroup):
    wait_captcha_state = State()
    null_state = State()  # idle when the user decided to leave the bot


class RegestrationState(StatesGroup):
    captcha_state = State()
    lang_choose_state = State()
    hello_state = State()
    proceed_state = State()
    follow_telegram_state = State()
    follow_twitter_state = State()
    submit_address_state = State()
    
    main_menu_state = State()  # State for the main menu
    lang_choose_state_again = State()  # changing the language second time
    yes_no_state = State()
    
    