"""Bot handlers
"""
import logging

from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InputFile

from src.bot import utils
from src.bot.dependencies import dp, config
from src.bot.states import QuizFlow, questions

logger = logging.getLogger(__name__)

QUIZ_BUTTON = KeyboardButton(text="Квиз")
RESULTS_BUTTON = KeyboardButton(text="Результаты")
THEORY_BUTTON = KeyboardButton(text="Справочник")


# todo add cancel command handler
# todo add logging

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """Main menu
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=False,
                                   row_width=1)
    keyboard.add(QUIZ_BUTTON, RESULTS_BUTTON, THEORY_BUTTON)

    await message.answer("Проверь свои знания!", reply_markup=keyboard)


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
async def show_theory(message: types.Message):
    """Menu for choosing theory topic
    """
    # keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
    #                                one_time_keyboard=True,
    #                                row_width=1)
    # keyboard.add(, )
    file = open(
        "C:\\Users\\Nikita\\Projects\\parasites_quiz\\src\\bot\\theory_1.pdf",
        "rb")
    await message.answer_document(file)


@dp.message_handler(filters.Text(equals=QUIZ_BUTTON.text))
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
            print(results)
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
