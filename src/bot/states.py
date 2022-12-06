"""States
"""
from dataclasses import dataclass
from typing import List, Optional

from aiogram.dispatcher.filters.state import StatesGroup, State


class QuizFlow(StatesGroup):
    """Flow of questions in quiz
    """
    q_1 = State()
    q_2 = State()
    q_3 = State()
    q_4 = State()
    q_10 = State()


@dataclass
class Options:
    image_path: Optional[str] = None  # Send image as well as question
    repeat_answers: Optional[
        bool] = None  # repeat available answers in message


@dataclass
class Question:
    text: str
    answers: List[str]
    correct_answer: List[str]
    options: Optional[Options] = Options()


questions = dict(
    q_1=Question(text="К паразитическим простейшим относятся:",
                 answers=[
                     '1) амёба протей',
                     '2) инфузория-туфелька',
                     '3) трипаносома',
                     '4) радиолярия',
                     '5) лямблия кишечная'
                 ],
                 correct_answer=['3) трипаносома', '5) лямблия кишечная']),
    q_2=Question(
        text="Заражение человека малярийным плазмодием происходит при "
             "попадании в "
             "его организм:",
        answers=[
            '1) крови комара',
            '2) слюны комара',
            '3) личинок комара',
            '4) яиц комара',
        ],
        correct_answer=['2) слюны комара']
    ),
    q_3=Question(text="Патогенное действие лямблии кишечной проявляется в:",
                 answers=[
                     '1) индукции сильных аллергических реакций организма '
                     'хозяина',
                     '2) ухудшении процессов всасывания в тонкой кишке',
                     '3) поражении кроветворных органов',
                     '4) прободении стенки толстой кишки'
                 ],
                 correct_answer=[
                     '2) ухудшении процессов всасывания в тонкой кишке'
                 ],
                 options=Options(repeat_answers=True)
                 ),
    q_4=Question(
        text="Специфическим переносчиком возбудителей лейшманиозов "
             "является насекомое отряда:",
        answers=[
            '1) перепончатокрылые',
            '2) двукрылые',
            '3) жесткокрылые',
            '4) полужесткокрылые'
        ],
        correct_answer=['2) двукрылые']),
    q_10=Question(
        text="Все представленные на рисунке организмы кроме одного "
             "являются паразитами. Определите под каким номером "
             "свободноживущий организм",
        answers=['1', '2', '3', '4'],
        correct_answer=['3'],
        options=Options(
            image_path="C:\\Users\\Nikita\\Projects\\parasites_quiz\\src"
                       "\\bot\\q_10.jpg")  # fixme
    ),
)
