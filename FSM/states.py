from aiogram.fsm.state import StatesGroup, State
from keyboards.small_kb import language_choose_kb, join_kb, sub_cancel_kb, social_join_kb
from keyboards.menu_kb import menu_kb
from messages.menu_messages import menu_messages
from messages.basic_messages import messages
from aiogram import types
class CaptchaState(StatesGroup):
    wait_captcha_state = State()
    null_state = State()  # idle when the user decided to leave the bot


class RegistrationState(StatesGroup):
    captcha_state = State()
    lang_choose_state = State()
    hello_state = State()
    proceed_state = State()
    follow_telegram_state = State()
    follow_twitter_state = State()
    submit_address_state = State()
    
    main_menu_state = State()  # State for the main menu
    menu_settings = State()  # State for the main menu
    lang_choose_state_again = State()  # changing the language second time
    yes_no_state = State()
    
class TasksState(StatesGroup):
    current_tasks_state = State()  # State for the all the tasks available
    single_task_state = State()  # State for the all the tasks available
    achievements_state = State()  # State for the all the tasks available


state_messages = {
    'RegistrationState:lang_choose_state': "LANGUAGE_CHOOSE",
    'RegistrationState:hello_state': "WELCOME_MESSAGE",
    'RegistrationState:proceed_state': "PROCEED_MESSAGE",
    'RegistrationState:follow_telegram_state': "MAKE_SURE_TELEGRAM",
    'RegistrationState:follow_twitter_state': "FOLLOW_TWITTER_TEXT",
    'RegistrationState:submit_address_state': "SUBMIT_ADDRESS_TEXT",
    'RegistrationState:main_menu_state': "MENU",
}
state_menus = {
    'RegistrationState:lang_choose_state': menu_messages,
    'RegistrationState:hello_state': messages,
    'RegistrationState:proceed_state': messages,
    'RegistrationState:follow_telegram_state': messages,
    'RegistrationState:follow_twitter_state': messages,
    'RegistrationState:submit_address_state': messages,
    'RegistrationState:main_menu_state': menu_messages,
}
state_keyboards = {
    ('RegistrationState:lang_choose_state', 'ENG'): language_choose_kb,
    ('RegistrationState:lang_choose_state', 'RU'): language_choose_kb,
    ('RegistrationState:hello_state', 'ENG'): join_kb['ENG'],
    ('RegistrationState:hello_state', 'RU'): join_kb['RU'],
    ('RegistrationState:proceed_state', 'ENG'): sub_cancel_kb['ENG'],
    ('RegistrationState:proceed_state', 'RU'): sub_cancel_kb['RU'],
    ('RegistrationState:follow_telegram_state', 'ENG'): social_join_kb['ENG'],
    ('RegistrationState:follow_telegram_state', 'RU'): social_join_kb['RU'],
    ('RegistrationState:follow_twitter_state', 'ENG'): types.ReplyKeyboardRemove(),
    ('RegistrationState:follow_twitter_state', 'RU'): types.ReplyKeyboardRemove(),
    ('RegistrationState:submit_address_state', 'ENG'): types.ReplyKeyboardRemove(),
    ('RegistrationState:submit_address_state', 'RU'): types.ReplyKeyboardRemove(),
    ('RegistrationState:main_menu_state', 'ENG'): menu_kb['ENG'],
    ('RegistrationState:main_menu_state', 'RU'): menu_kb['RU'],
}


def get_state_from_string(state_string):
    parts = state_string.split(':')
    if len(parts) == 2:
        class_name, state_name = parts
        # Assuming the class is defined in the current module or properly imported
        module = globals()  # Gets a dictionary of global symbol table
        state_class = module.get(class_name)  # Get the class by name
        
        if state_class:
            return getattr(state_class, state_name, None)  # Get the state from the class
    return None

def get_clean_state_identifier(state):
    full_str = str(state)
    # Typically, the format is "<State 'RegistrationState:lang_choose_state'>"
    # We need to remove the "<State '" prefix and "'>" suffix.
    clean_identifier = full_str.split("'")[1]  # This splits the string by single quotes and takes the second element
    return clean_identifier

