from tkinter import *

try:  # When used as a package
    from NepalStockTracker.Assets import Assets

except ImportError:  # When used as a normal script
    from Assets import Assets


class _Entry:
    '''
    An Entry widget having a placeholder text like of HTML. When user
    focuses to the entry widget then the placeholder text gets removed.
    When user focuses out of that Entry widget without entering any value
    then the placeholder text gets inserted.
    '''

    def __init__(self, frame, DefaultText, bg='black', width=19, show='', PasswordVisible=None):
        '''
        param:
            frame               : Obj Frame to keep Entry widget
            DefaultText         : Default text for each Entry widget
            bg                  : Background color for frame
            width               : Width for Entry widget
            show                : Used to display ● in Password Entry widget
            PasswordVisible     : Hide text when True
        '''

        self.show = show
        self.frame = frame
        self.IsDefault = True
        self.DefaultText = DefaultText
        self.PasswordVisible = PasswordVisible
        self.style_name = f'{DefaultText}.TEntry'

        self.var = StringVar()
        self.var.set(self.DefaultText)

        self.Frame = Frame(frame, bg=bg)
        self.Entry = Entry(self.Frame, textvariable=self.var, width=width, justify='center')
        self.Entry.pack(ipady=5)
        self.Entry.config(fg='grey')
        self.LineFrame = Frame(self.Frame, height=5, bg='#9da17d')
        self.LineFrame.pack(fill='x')

        self.Entry.bind('<FocusIn>', self.FocusIn)
        self.Entry.bind('<FocusOut>', self.FocusOut)

    def FocusIn(self, event=None):
        '''
        When Entry gets focus either by click to it or by pressing TAB key
        '''

        self.LineFrame.config(bg='#02c4f5')

        if self.IsDefault and self.var.get().strip() == self.DefaultText:
            self.var.set('')
            self.IsDefault = False
            self.Entry.config(fg='black')

            if self.PasswordVisible and self.PasswordVisible.IsHidden:
                self.Entry.config(show=self.show)

    def FocusOut(self, event=None):
        '''
        When Entry gets focus out either by click to another widget or by
        pressing TAB key
        '''

        self.LineFrame.config(bg='#9da17d')

        if self.IsDefault is False and not self.var.get().strip():
            self.IsDefault = True

            self.Entry.config(fg='grey')
            self.var.set(self.DefaultText)

            if self.PasswordVisible and self.PasswordVisible.IsHidden:
                self.Entry.config(show='')

    def SetToDefault(self):
        '''
        Set the default values to respective Entry when user finish adding,
        deleting or renaming values
        '''

        self.IsDefault = True

        if self.show is not None:
            self.show = True
            self.Entry.config(show='')

        self.var.set(self.DefaultText)
        self.Entry.config(fg='grey')


class _Password_Entry:
    '''
    An Entry widget having placeholder text "●". Also draw button that hide
    or show the text when clicked.
    '''

    def __init__(self, frame, DefaultText, bg, width=19):
        '''
        param:
            frame           : Obj Frame to keep Entry widget
            DefaultText    : Default text for each Entry widget
            bg              : Background color for frame
            width           : Width for Entry widget
            show            : Used to display ● in Password Entry widget
        '''

        self.Assets = Assets()
        self.IsPasswordHidden = PasswordVisible()

        self.bg = bg
        self.show = '●'
        self.width = width
        self.frame = frame
        self.DefaultText = DefaultText

        self.PasswordFrame = Frame(self.frame, bg=self.bg)

        self.PasswordEntry = _Entry(self.PasswordFrame, self.DefaultText, show=self.show, width=width, bg=self.bg, PasswordVisible=self.IsPasswordHidden)
        self.PasswordEntry.Frame.pack(side=LEFT)
        self.ShowHidePassword = Button(self.PasswordFrame, image=self.Assets.HidePasswordImage, bd=0, bg=self.bg, activebackground=self.bg, cursor='hand2', takefocus=False, command=self.ShowHidePasswordCommand)
        self.ShowHidePassword.pack(side=RIGHT, padx=(5, 0))

    def ShowHidePasswordCommand(self):
        '''
        Toggle between "●" and text when user clicks to hide-show-password button
        '''

        if self.IsPasswordHidden.IsHidden:
            self.IsPasswordHidden.IsHidden = False
            self.PasswordEntry.Entry.config(show='')
            self.ShowHidePassword.config(image=self.Assets.ShowPasswordImage)

        else:
            self.IsPasswordHidden.IsHidden = True

            if self.PasswordEntry.IsDefault is False:
                self.PasswordEntry.Entry.config(show=self.show)

            self.ShowHidePassword.config(image=self.Assets.HidePasswordImage)


class PasswordVisible:
    '''
    Set IsHidden attribute to True when password is not shown
    else set it to False
    '''

    def __init__(self):
        self.IsHidden = True
