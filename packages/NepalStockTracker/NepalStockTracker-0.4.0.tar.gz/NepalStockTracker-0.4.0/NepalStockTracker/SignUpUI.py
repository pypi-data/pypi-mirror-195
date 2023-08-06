from tkinter import *
from tkinter.font import Font
from tkinter import messagebox

try:  # When used as a package
    from NepalStockTracker.db import DB
    from NepalStockTracker import Include
    from NepalStockTracker.Assets import Assets
    from NepalStockTracker._Entry import _Entry, _Password_Entry
    from NepalStockTracker.PasswordConditions import PasswordConditions
    from NepalStockTracker.SecurityQuestionUI import SecurityQuestionUI

except ImportError:  # When used as a normal script
    import Include
    from db import DB
    from Assets import Assets
    from _Entry import _Entry, _Password_Entry
    from PasswordConditions import PasswordConditions
    from SecurityQuestionUI import SecurityQuestionUI


class SignUpUI:
    '''
    Show widgets to create new account
    '''

    def __init__(self, master, MainFrame, Login, MainFrameBg):
        self.Assets = Assets()
        self.RightBG = '#e3be02'
        self.MainFrameBg = MainFrameBg

        self.Login = Login
        self.master = master
        self.MainFrame = MainFrame
        self.IsPasswordHidden = True

    def ShowWidgets(self, event):
        '''
        Show corresponding widgets
        '''

        self.master.withdraw()

        self.MainFrame.pack_forget()
        self.master.title('Nepal Stock Tracker | SIGN-UP')

        self.SignupFrame = Frame(self.master, bg=self.RightBG)
        self.SignupFrame.pack()

        self.LeftFrame = Frame(self.SignupFrame)
        self.LeftFrame.pack(side=LEFT)
        self.RightFrame = Frame(self.SignupFrame, bg=self.RightBG)
        self.RightFrame.pack(side=RIGHT)

        self.LeftImage = Label(self.LeftFrame, image=self.Assets.SignUpFrameImage, bg='#e3be02')
        self.LeftImage.pack(ipadx=50, ipady=50)

        self.UsernameEntry = _Entry(self.RightFrame, 'Username', width=63, bg=self.RightBG)
        self.UsernameEntry.Frame.pack(pady=(10, 0), ipady=5)

        self.PassFrame = Frame(self.RightFrame, bg=self.RightBG)
        self.PassFrame.pack()
        self.PasswordEntry = _Password_Entry(self.PassFrame, 'Password', width=63, bg=self.RightBG)
        self.PasswordEntry.PasswordFrame.pack(padx=(48, 0))

        self.ConfirmPassFrame = Frame(self.RightFrame, bg=self.RightBG)
        self.ConfirmPassFrame.pack()
        self.ConfirmPasswordEntry = _Password_Entry(self.ConfirmPassFrame, 'Confirm Password', self.RightBG, 63)
        self.ConfirmPasswordEntry.PasswordFrame.pack(pady=10, padx=(48, 0))

        self.PasswordHints = PasswordConditions(self.master, self.PassFrame, self.PasswordEntry.PasswordEntry, self.ConfirmPasswordEntry.PasswordEntry, self.ConfirmPassFrame, self.RightBG)
        self.PasswordHints.Frame.pack()

        self.SecurityQuestionsUI = SecurityQuestionUI(self.master, self.RightFrame, pady=10, bg=self.RightBG)
        self.SecurityQuestionsUI.frame.pack()

        self.SubmitButton = Button(self.RightFrame, image=self.Assets.SubmitImage, bg=self.RightBG, activebackground=self.RightBG, activeforeground="white", bd='0', cursor='hand2', font=Font(size=10, weight='bold'), command=self.SubmitButtonCommand)
        self.SubmitButton.pack(pady=(0, 10), ipady=5)

        self.BackButton = Button(self.RightFrame, image=self.Assets.BackImage, bd=0, cursor='hand2', bg=self.RightBG, activebackground=self.RightBG, command=self.BackButtonCommand)
        self.BackButton.pack(pady=(30, 0))

        Include.SetWindowPosition(self.master)

    def SubmitButtonCommand(self):
        '''
        When user clicks submit button
        '''

        UserNameDefault = self.UsernameEntry.IsDefault
        PasswordDefault = self.PasswordEntry.PasswordEntry.IsDefault
        ConfirmPasswordDefault = self.ConfirmPasswordEntry.PasswordEntry.IsDefault
        SecurityQuestionAnswerDefault = self.SecurityQuestionsUI.SecurityQuestionAnswerEntry.IsDefault

        password = self.PasswordEntry.PasswordEntry.var.get().strip()
        ConfirmPassword = self.ConfirmPasswordEntry.PasswordEntry.var.get().strip()

        username = self.UsernameEntry.var.get().strip()
        SecurityQuestion = self.SecurityQuestionsUI.ComboBox.ComboVar.get()

        if any([UserNameDefault, PasswordDefault, SecurityQuestionAnswerDefault, ConfirmPasswordDefault]):
            messagebox.showerror('Invalid', 'Provide valid values')

        elif SecurityQuestion not in self.SecurityQuestionsUI.ComboValues:
            messagebox.showerror('Invalid', 'Select valid SECURITY QUESTION')

        elif DB().UserExists(username):
            messagebox.showerror('ERR', 'Username already exists')

        elif len(username) < 5:
            messagebox.showerror('ERR', 'Username must be at least 5 characters long')

        elif self.PasswordHints.IsPasswordStrong is False:
            messagebox.showerror('ERR', 'Password does not meet requirements')

        elif password != ConfirmPassword:
            messagebox.showerror('ERR', 'Passwords are incorrect')

        else:
            answer = self.SecurityQuestionsUI.SecurityQuestionAnswerEntry.var.get().lower()
            DB().AddNewUser(username, SecurityQuestion, answer, password)

            messagebox.showinfo('Success', 'Account has been created!!!\n\nEnter credentials to LOGIN-IN')
            self.SignupFrame.destroy()
            self.Login.ShowWidgets()

    def BackButtonCommand(self):
        '''
        Send user to first window when user clicks to back button
        '''

        self.master.title('Nepal Stock Tracker')

        self.SignupFrame.destroy()
        self.MainFrame.pack(padx=50, pady=50)
