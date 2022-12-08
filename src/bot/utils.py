"""Utility functions
"""
import json
import logging
from json import JSONDecodeError
from pathlib import Path
from typing import List, Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.states import questions, Question
from src.config import Config

logger = logging.getLogger(__name__)


class ResultsUnavailable(Exception):
    """Raise when can not get results
    """


def count_score(user_answers: dict) -> int:
    """Count how many correct answers user gave.
    Returns integer of correct answers
    """
    count = 0
    for question_number, answer in user_answers.items():
        correct_answer = questions.get(question_number).correct_answer
        if answer == correct_answer:
            count += 1
    return count


def read_results(config: Config) -> dict:
    """Read from json file results
    """
    try:
        with open(config.logs_path/Path("results.json"), "r", encoding="utf-8") as file:
            results = json.load(file)
    except (FileNotFoundError, JSONDecodeError) as err:
        logger.error(f"Error reading results: {err}")
        raise ResultsUnavailable
    return results


def save_results(config: Config, results: dict) -> None:
    """Save new version of results
    """
    try:
        with open(config.logs_path/Path("results.json"), 'w',
                  encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
    except (FileNotFoundError, JSONDecodeError) as err:
        logger.error(f"Error saving results: {err}")
        logger.info(f"Results not saved: {results}")


def create_answers_keyboard(question: Question,
                            exclude_answers: Optional[List[str]] = None) \
        -> InlineKeyboardMarkup:
    """Create inline keyboard that consists of available answers
    and next button"""

    inline_keyboard = InlineKeyboardMarkup()
    if not exclude_answers:  # костыльно
        exclude_answers = []

    for index, answer in enumerate(question.answers):
        # skip answer
        if answer in exclude_answers:
            continue

        inline_keyboard.add(
            InlineKeyboardButton(text=answer,
                                 callback_data=f'a|{index}')
        )
    inline_keyboard.add(InlineKeyboardButton(text="Следующий вопрос ➡️",
                                             callback_data=f"n|"))

    return inline_keyboard


def format_question_text(question: Question, question_index: str) -> str:
    """Format question text, check for additional options
    :parameter question - Questions object
    :parameter question_index - str in a form (q_1)
    :returns str in html formatted way
    """
    q_number = number_from_index(question_index)

    header = f"👉 <b>Вопрос №{q_number}</b>: "

    if question.options.repeat_answers:
        extra = "\n\n<i>Варианты ответа</i>:\n"
        for answer in question.answers:
            extra += f"{answer}\n"
    else:
        extra = "\n"

    return header + question.text + extra


def format_results_text(user_answers: dict, include_header: bool = True):
    """Format in HTML style results
    """
    correct_answers = count_score(user_answers)

    header = "👍 Вы ответили на все вопросы викторины!\n"
    result = f"Правильных ответов: <b>{correct_answers}</b> " \
             f"из <b>{len(questions)}</b>\n"
    details = "<i>Подробности</i>:\n"
    for _index, question in questions.items():
        q_number = number_from_index(_index)
        correct = user_answers.get(_index) == question.correct_answer
        emoji = "✅" if correct else "❌"
        details += f"Вопрос {q_number} - {emoji}\n"

    if include_header:
        return header + result + details
    return result + details


def format_all_users_stats(results: dict) -> str:
    """Count stats for all users and format in html friendly way"""
    totals = results["total"]
    total_participants = len(totals)
    if total_participants == 0:
        return "\nОго! Еще никто не принимал участия в квизе, " \
               "у вас есть возможность стать первым!"
    average_mark = sum(totals.values()) / total_participants

    header = "\n<i>Статистика:</i>\n"
    stats = f"Всего участников квиза - {total_participants}\n" \
            f"Среднее количество правильных ответов - {average_mark:.2f}"
    return header + stats


def number_from_index(index: str) -> int:
    """Get question number from index in a form (q_1, q_12, etc)
    """
    return int(index.split("_")[1])
