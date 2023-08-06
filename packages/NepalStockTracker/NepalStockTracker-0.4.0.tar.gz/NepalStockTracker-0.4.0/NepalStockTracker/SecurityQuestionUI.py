from tkinter import *
import tkinter.ttk as ttk

try:  # When used as a package
    from NepalStockTracker._Entry import _Entry
    from NepalStockTracker._ComboBox import _ComboBox

except ImportError:  # When used as a normal script
    from _Entry import _Entry
    from _ComboBox import _ComboBox


class SecurityQuestionUI:
    '''
    Show ComboBox widget containing different questions and Entry widget to
    enter the answer to the corresponding question
    '''

    def __init__(self, win, frame, bg, pady=10):
        self.win = win
        self.frame = Frame(frame, bg=bg)

        self.ComboValues = [
            'In what city were you born?',
            'What high school did you attend?',
            'What was your childhood nickname?',
            'What was the make of your first car?',
            'What is the name of your favorite pet?',
            'What was your favorite food as a child?',
            'In what city or town was your first job?',
            'What year was your father (or mother) born?',
            'What is your oldest sibling\'s middle name?',
            'What was the name of your elementary school?',
            'Where were you when you had your first kiss?',
            'In what city does your nearest sibling live?',
            'What was the name of your first stuffed animal?',
            'What was the last name of your third grade teacher?',
            'What is the name of your favorite childhood friend?',
            'In what city or town did your mother and father meet?',
            'In what city did you meet your spouse/significant other?',
            'What is the name of the place your wedding reception was held?',
            'What is the first name of the boy or girl that you first kissed?',
            'What is the name of a college you applied to but didn\'t attend?'
        ]

        self.ComboBox = _ComboBox(win, self.frame, self.ComboValues, DEFAULT_TEXT='SECURITY QUESTION', width=60)
        self.ComboBox.ComboBox.pack(pady=(0, pady), ipady=5)

        self.SecurityQuestionAnswerEntry = _Entry(self.frame, 'Security Question Answer', width=63, bg=bg)
        self.SecurityQuestionAnswerEntry.Frame.pack(pady=(0, pady))
