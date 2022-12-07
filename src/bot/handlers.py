"""Bot handlers
"""
import logging

from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InputFile, InlineKeyboardMarkup, InlineKeyboardButton


from src.bot import utils
from src.bot.dependencies import dp, config, bot
from src.bot.states import QuizFlow, questions, theory_materials

logger = logging.getLogger(__name__)

QUIZ_BUTTON = KeyboardButton(text="Квиз")
RESULTS_BUTTON = KeyboardButton(text="Результаты")
THEORY_BUTTON = KeyboardButton(text="Справочник")
HELP_BUTTON = KeyboardButton(text="Помощь")

MAIN_MENU = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=False,
                                row_width=2)
MAIN_MENU.add(QUIZ_BUTTON, RESULTS_BUTTON, THEORY_BUTTON, HELP_BUTTON)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """Main menu
    """
    await message.answer("Проверь свои знания!", reply_markup=MAIN_MENU)


@dp.message_handler((filters.Text(equals=HELP_BUTTON.text)))
async def show_help(message: types.Message):
    """Show help message
    """
    text = "<b>Помощь по командам бота</b>:\n" \
           "/start - вызвать главное меню\n" \
           "/quiz или кнопка 'Квиз' в меню - начать прохождение викторины\n" \
           "<b>Примечание</b>: когда вы выполняете квиз, " \
           "остальные команды становятся недоступны " \
           "до завершения прохождения. " \
           "Чтобы выйти из режима квиза, не пройдя его до конца, " \
           "используйте команду <b>/cancel</b>"
    await message.answer(text, parse_mode="HTML")


@dp.message_handler(filters.Text(equals=RESULTS_BUTTON.text))
async def show_results(message: types.Message):
    """Show results
    """
    all_results = utils.read_results(config=config)
    user_answers = all_results["results"].get(str(message.from_user.id))
    if not user_answers:
        text = "Вы пока не принимали участия в квизе!\n"
    else:
        text = utils.format_results_text(user_answers, include_header=False)

    stats = utils.format_all_users_stats(results=all_results)

    await message.answer(text=text + stats, parse_mode="HTML")


@dp.message_handler(filters.Text(equals=THEORY_BUTTON.text))
async def show_theory_menu(message: types.Message):
    """Menu for choosing theory topic
    """
    inline_keyboard = InlineKeyboardMarkup()
    text = "По какой теме хотите освежить свои знания? 🤓"
    for _index, theory_material in theory_materials.items():
        inline_keyboard.add(InlineKeyboardButton(
            text=theory_material.button_text,
            callback_data=f"show_theory|{_index}"
        ))
    await message.answer(text=text, reply_markup=inline_keyboard)


@dp.message_handler(filters.Text(equals=QUIZ_BUTTON.text))
@dp.message_handler(commands='quiz')
async def start_quiz(message: types.Message):
    """Entry point into quiz
    """
    # Init quiz flow from question 1
    await QuizFlow.q_1.set()
    question = questions.get('q_1')

    inline_keyboard = utils.create_answers_keyboard(question)

    await message.answer(text=utils.format_question_text(question,
                                                         question_index="q_1"),
                         reply_markup=inline_keyboard,
                         parse_mode="HTML")


@dp.message_handler(commands='cancel', state="*")
async def cancel_quiz(message: types.Message, state: FSMContext):
    """Exit quiz mode
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    await message.reply(
        'Выход из режима квиза. Сожалеем, что вы не завершили прохождение, '
        'но всегда можно сделать это позднее! 😉',
        reply_markup=MAIN_MENU
    )


@dp.callback_query_handler(filters.Text(startswith="a|"), state="*")
async def add_answer(callback: types.CallbackQuery, state: FSMContext):
    """Add to message with question selected answer"""
    await callback.answer()

    _, answer_index = callback.data.split('|')

    async with state.proxy() as data:
        current_question_index = data.state.split(':')[1]
        question = questions.get(current_question_index)
        # get text of user answer using answer_index
        user_answer = question.answers[int(answer_index)]

        if data.get(current_question_index):
            data[current_question_index].append(user_answer)
        else:
            data[current_question_index] = [user_answer]
        already_answered = data[current_question_index]

    inline_keyboard = utils.create_answers_keyboard(
        question,
        exclude_answers=already_answered
    )

    text = utils.format_question_text(question,
                                      question_index=current_question_index)
    text += '\n<i>Ваши ответы</i>:\n'
    for user_answer in data.get(current_question_index):
        text += f'{user_answer}\n'
    await callback.message.edit_text(text=text,
                                     reply_markup=inline_keyboard,
                                     parse_mode="HTML")


@dp.callback_query_handler(filters.Text(startswith="n|"), state="*")
async def next_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    # remove keyboard on previous message
    await callback.message.edit_reply_markup(reply_markup=None)

    user_id = str(callback.from_user.id)
    await QuizFlow.next()  # move to next question

    async with state.proxy() as data:
        # finish quiz
        if data.state is None:
            # Memorize result and finish quiz
            results = utils.read_results(config)
            user_answers = data.as_dict()

            results['results'][user_id] = user_answers
            results['total'][user_id] = utils.count_score(user_answers)
            utils.save_results(config, results)

            result_text = utils.format_results_text(user_answers)
            await callback.message.answer(result_text, parse_mode="HTML")
            await state.finish()
            return

    # continue quiz
    question_index = data.state.split(':')[1]
    question = questions.get(question_index)
    inline_keyboard = utils.create_answers_keyboard(question)

    if question.options.image_path is not None:
        await callback.message.answer_photo(
            InputFile(path_or_bytesio=question.options.image_path)
        )
    text = utils.format_question_text(question,
                                      question_index=question_index)
    await callback.message.answer(text=text,
                                  reply_markup=inline_keyboard,
                                  parse_mode="HTML")


@dp.callback_query_handler(filters.Text(startswith="show_theory"))
async def show_theory(callback: types.CallbackQuery):
    """Send user a pdf file with requested theory
    """
    await callback.answer()
    _index = callback.data.split('|')[1]
    theory_material = theory_materials.get(_index)
    await callback.message.answer_document(
        InputFile(theory_material.file_path),
        caption=f"{theory_material.button_text}"
    )


@dp.errors_handler()
async def log_errors(update: types.Update, error):
    """send errors to tg control chat
    """
    msg = f"Error happened: {error}"
    await bot.send_message(chat_id=config.control_chat_id, text=msg)
