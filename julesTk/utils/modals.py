"""Classes for creating basic modal dialogs

Such as YES-NO, Question, Information dialogs etc.

"""

from julesTk import view, controller
from julesTk.view.window import ModalWindow
from julesTk.dialog.simple import *
from julesTk.dialog.question import *

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"

__all__ = [
    "ModalWindow",
    "MessageBox", "inform",
    "QuestionBox", "ask_question"
]
