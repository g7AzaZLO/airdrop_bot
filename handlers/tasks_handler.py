from aiogram import types
from FSM.states import TasksState

from aiogram.fsm.context import FSMContext
from handlers.standart_handler import get_message

from messages.menu_messages import menu_messages
from keyboards.small_kb import kb_task_done_back

from DB.database_logic import get_language_for_user
from handlers.state_handler import state_handler_router



@state_handler_router.message(TasksState.current_tasks_state)
async def current_tasks_handler(message: types.Message, state: FSMContext) -> None:
	print(f"def current_tasks_handler, task #{message.text}")
	reply = "HERE IS YOUR TASK:"  # TODO add to the messages file
	language = await get_language_for_user(message.from_user.id)
	await message.answer(text=reply, reply_markup=kb_task_done_back[language])  # TODO wrong place for keyboard
	await state.set_state(TasksState.single_task_state)
	return


@state_handler_router.message(TasksState.single_task_state)
async def single_task_handler(message: types.Message, state: FSMContext) -> None:
	print(f"def single_task_handler")
	language = await get_language_for_user(message.from_user.id)
	user_response = message.text
	if user_response in ["✅Выполнил", "✅Done"]:
		reply = "GREAT JOB"  # TODO add to the messages file
		await message.answer(text=reply)
		return
	elif user_response in ["⏪Вернуться Назад", "⏪Return Back"]:
		reply = "ALL TASKS"  # TODO add to the messages file
		await message.answer(text=reply)
		return
	else:
		reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
		await message.answer(text=reply, reply_markup=kb_task_done_back[language])
		# await state.set_state(RegistrationState.main_menu_state)
		return
