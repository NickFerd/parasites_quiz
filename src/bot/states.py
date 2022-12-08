"""States
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from aiogram.dispatcher.filters.state import StatesGroup, State

from src.bot.dependencies import config


class QuizFlow(StatesGroup):
    """Flow of questions in quiz
    """
    q_1 = State()
    q_2 = State()
    q_3 = State()
    q_4 = State()
    q_5 = State()
    q_6 = State()
    q_7 = State()
    q_8 = State()
    q_9 = State()
    q_10 = State()


@dataclass
class Options:
    image_path: Optional[str] = None  # Send image as well as question
    repeat_answers: Optional[bool] = None  # repeat available answers in text
    check_answer_order: Optional[bool] = False  # whether answers order matter


@dataclass
class Question:
    text: str
    answers: List[str]
    correct_answer: List[str]
    options: Optional[Options] = Options()


@dataclass
class Theory:
    button_text: str
    file_path: str


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
    q_5=Question(
        text="Окончательным хозяином возбудителя малярии является:",
        answers=[
            "1) малярийный плазмодий",
            "2)	личинка малярийного комара",
            "3)	малярийный комар",
            "4)	человек, больной малярией"
        ],
        correct_answer=["3)	малярийный комар"],
    ),
    q_6=Question(
        text="Установите последовательность процессов в жизненном цикле "
             "малярийного плазмодия, "
             "начиная с передачи паразита в тело промежуточного хозяина",
        answers=[
            "1) поступление плазмодия в клетки печени",
            "2) проникновение возбудителя в кровяное русло",
            "3) укус человека незараженным комаром",
            "4) множественное деление паразита в эритроцитах",
            "5) половое размножение плазмодия в теле основного хозяина"
        ],
        correct_answer=[
            "2) проникновение возбудителя в кровяное русло",
            "1) поступление плазмодия в клетки печени",
            "4) множественное деление паразита в эритроцитах",
            "3) укус человека незараженным комаром",
            "5) половое размножение плазмодия в теле основного хозяина"
        ],
        options=Options(check_answer_order=True)
    ),
    q_7=Question(
        text="Установите последовательность стадий в жизненном цикле "
             "малярийного плазмодия, начиная с образования гамет. "
             "Запишите соответствующую последовательность цифр",
        answers=[
            "1) размножение в эритроцитах",
            "2) заражение человека",
            "3) размножение в клетках печени человека",
            "4) бесполое размножение в организме комара",
            "5) образование зиготы",
            "6) образование гамет"
        ],
        correct_answer=[
            "6) образование гамет",
            "5) образование зиготы",
            "4) бесполое размножение в организме комара",
            "2) заражение человека",
            "3) размножение в клетках печени человека",
            "1) размножение в эритроцитах"
        ],
        options=Options(check_answer_order=True)
    ),
    q_8=Question(
        text="Какие из перечисленных заболеваний относят "
             "к «болезням грязных рук»?",
        answers=[
            "1) дизентерия",
            "2) цинга",
            "3) СПИД",
            "4) лямблиоз",
            "5) сахарный диабет",
            "6) герпес"
        ],
        correct_answer=[
            "1) дизентерия",
            "4) лямблиоз"
        ]
    ),
    q_9=Question(
        text="Установите соответствия между заболеванием "
             "и его географическим распространением. Амёбная дизентерия:",
        answers=[
            "1) Экваториальная Африка",
            "2) Латинская Америка",
            "3) повсеместно",
            "4) Индия, Пакистан, Бангладеш"
        ],
        correct_answer=["3) повсеместно"]
    ),
    q_10=Question(
        text="Все представленные на рисунке организмы, кроме одного, "
             "являются паразитами. Определите под каким номером "
             "свободноживущий организм",
        answers=['1', '2', '3', '4'],
        correct_answer=['3'],
        options=Options(
            image_path=config.assets_path / Path("q_10.jpg"))
    ),
)

theory_materials = dict(
    theory_1=Theory(button_text="Дизентерийная амеба",
                    file_path=config.assets_path / Path("theory_1.pdf")),
    theory_2=Theory(button_text="Лямблия кишечная",
                    file_path=config.assets_path / Path("theory_2.pdf")),
    theory_3=Theory(button_text="Род Лейшмания",
                    file_path=config.assets_path / Path("theory_3.pdf")),
    theory_4=Theory(button_text="Род Трипаносома",
                    file_path=config.assets_path / Path("theory_4.pdf")),
    theory_5=Theory(button_text="Малярийный плазмодий",
                    file_path=config.assets_path / Path("theory_5.pdf")),
)
