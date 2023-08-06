import hashlib
from tkinter import *
from tkinter.font import Font
from tkinter import messagebox

try:  # When used as a package
    from NepalStockTracker.db import DB
    from NepalStockTracker import Include
    from NepalStockTracker._Entry import _Entry
    from NepalStockTracker.Assets import Assets
    from NepalStockTracker.NewPasswordUI import NewPasswordUI
    from NepalStockTracker.SecurityQuestionUI import SecurityQuestionUI

except ImportError:  # When used as a normal script
    import Include
    from db import DB
    from Assets import Assets
    from _Entry import _Entry
    from NewPasswordUI import NewPasswordUI
    from SecurityQuestionUI import SecurityQuestionUI


class ForgotPasswordUI:
    '''
    Display widgets to get corresponding credentials to reset the password
    '''

    def __init__(self, master, LoginFrame):
        '''
        param:
            master      : Object of Tk
            LoginFrame  : Frame used to place Login widgets
        '''

        self.bg = '#cbd0d6'
        self.Assets = Assets()
        self.RightBG = '#aaff00'

        self.master = master
        self.LoginFrame = LoginFrame

    def ShowWidgets(self, event):
        '''
        Show corresponding widgets
        '''

        self.master.withdraw()

        self.LoginFrame.pack_forget()
        self.master.title('Nepal Stock Tracker | Reset Password')

        self.ForgotPasswordFrame = Frame(self.master, bg=self.RightBG)
        self.ForgotPasswordFrame.pack()

        self.LeftFrame = Frame(self.ForgotPasswordFrame)
        self.LeftFrame.pack(side=LEFT)
        self.RightFrame = Frame(self.ForgotPasswordFrame, bg=self.RightBG)
        self.RightFrame.pack(side=RIGHT, ipadx=50, pady=(50, 0))
        self.InnerRightFrame = Frame(self.RightFrame, bg=self.RightBG)
        self.InnerRightFrame.pack()

        self.LeftImage = Label(self.LeftFrame, image=self.Assets.ForgotPasswordFrameImage, bg='#aaff00')
        self.LeftImage.pack(ipady=3)

        self.UsernameEntry = _Entry(self.InnerRightFrame, 'Username', width=62, bg=self.RightBG)
        self.UsernameEntry.Frame.pack(ipady=5)

        self.SecurityQuestion = SecurityQuestionUI(self.master, self.InnerRightFrame, bg=self.RightBG)
        self.SecurityQuestion.frame.pack()

        self.ResetButton = Button(self.InnerRightFrame, image=self.Assets.ResetImage, fg='white', bg=self.RightBG, activebackground=self.RightBG, activeforeground="white", bd='0', cursor='hand2', font=Font(size=10, weight='bold'), command=self.ResetButtonCommand)
        self.ResetButton.pack(ipady=8)

        self.BackButton = Button(self.InnerRightFrame, image=self.Assets.BackImage, bd=0, cursor='hand2', bg=self.RightBG, activebackground=self.RightBG, command=self.BackButtonCommand)
        self.BackButton.pack(pady=(20, 0))

        Include.SetWindowPosition(self.master)

        self.UsernameEntry.Entry.bind('<Return>', self.ResetButtonCommand)
        self.SecurityQuestion.SecurityQuestionAnswerEntry.Entry.bind('<Return>', self.ResetButtonCommand)

    def ResetButtonCommand(self, event=None):
        '''
        When user clicks reset button after entering credentials
        '''

        UsernameEntryDefault = self.UsernameEntry.IsDefault
        SecurityQuestionEntryDefault = self.SecurityQuestion.SecurityQuestionAnswerEntry.IsDefault

        username = self.UsernameEntry.var.get().strip()
        SecurityQuestionCombo = self.SecurityQuestion.ComboBox.ComboVar.get().strip()
        SecurityAnswer = self.SecurityQuestion.SecurityQuestionAnswerEntry.var.get().strip().lower()

        ResetDetails = DB().ResetDetails(username)

        if any([UsernameEntryDefault, SecurityQuestionEntryDefault]) or SecurityQuestionCombo not in self.SecurityQuestion.ComboValues:
            messagebox.showerror('ERR', 'Provide valid information')

        elif ResetDetails is False:
            messagebox.showerror('ERR', f'Username: "{username}" not found')

        else:
            EncryptedSecurityAnswer = hashlib.sha256(SecurityAnswer.encode()).hexdigest()
            EncryptedSecurityQuestion = hashlib.sha256(SecurityQuestionCombo.encode()).hexdigest()

            if EncryptedSecurityQuestion not in ResetDetails or EncryptedSecurityAnswer not in ResetDetails:
                messagebox.showerror('ERR', 'Invalid Security Question or Security Answer')

            else:
                NewPassword = NewPasswordUI(username, self.master, self.ForgotPasswordFrame, self.LoginFrame, self.RightFrame, self.InnerRightFrame)
                NewPassword.ShowWidgets()

    def BackButtonCommand(self):
        '''
        When user clicks back button
        '''

        self.ForgotPasswordFrame.destroy()
        self.LoginFrame.pack()
