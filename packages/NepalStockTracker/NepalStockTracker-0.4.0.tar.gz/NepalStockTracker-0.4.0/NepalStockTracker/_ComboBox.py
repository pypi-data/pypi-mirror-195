import timeit
from tkinter import *
import tkinter.ttk as ttk


class _ComboBox:
    '''
    A combo-box with the list of fetched company names with auto-complete
    functionality.
    '''

    def __init__(self, master, frame, values, DEFAULT_TEXT='COMPANY SYMBOL', width=41):
        '''
        param:
            master      : Object of Tk
            frame       : Frame to place combo-box
            values      : Values for combo-box
        '''

        self.master = master
        self.frame = frame

        self.values = values
        self.StartTimer = None

        self.StartTimer = 0
        self.PreviousSearch = ''
        self.LocalSearchIndex = 0

        self.DEFAULT_TEXT = DEFAULT_TEXT

        self.ComboVar = StringVar()
        self.ComboVar.set(self.DEFAULT_TEXT)

        self.ComboBox = ttk.Combobox(self.frame, textvariable=self.ComboVar, values=self.values, width=width, justify='center', state='readonly')

        self.ComboBox.config(values=self.values)
        self.ComboBox.bind('<Button-1>', self.SingleClick)
        self.ComboBox.bind('<KeyRelease>', self.AutoComplete)

    def SingleClick(self, event):
        '''
        When user clicks to Combobox
        '''

        self.ComboBox.event_generate('<Down>', when='head')

    def AutoComplete(self, event=None):
        '''
        Search value when the focus is in ttk.Combobox
        '''

        _char = event.char.upper()

        if _char == '':
            return 'break'

        if self.StartTimer:
            end_timer = timeit.default_timer()
            escaped = end_timer - self.StartTimer

            if 0 < escaped < 0.27:
                _char = self.PreviousSearch + _char

        CommonNames = list(filter(lambda item: item.startswith(_char), self.values))

        if self.PreviousSearch != _char or self.LocalSearchIndex == len(CommonNames) - 1:
            self.LocalSearchIndex = 0

        self.PreviousSearch = _char
        self.StartTimer = timeit.default_timer()

        if CommonNames:
            self.ToSelectValue = CommonNames[self.LocalSearchIndex]
            self.LocalSearchIndex += 1

            self.ComboBox.set(self.ToSelectValue)
            self.ComboVar.set(self.ToSelectValue)
