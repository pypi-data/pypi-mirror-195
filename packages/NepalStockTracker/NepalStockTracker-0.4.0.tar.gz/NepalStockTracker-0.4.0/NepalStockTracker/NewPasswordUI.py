from tkinter import *
from tkinter.font import Font
from tkinter import messagebox

try:  # When used as a package
    from NepalStockTracker.db import DB
    from NepalStockTracker.Assets import Assets
    from NepalStockTracker._Entry import _Password_Entry
    from NepalStockTracker.PasswordConditions import PasswordConditions

except ImportError:  # When used as a normal script
    from db import DB
    from Assets import Assets
    from _Entry import _Password_Entry
    from PasswordConditions import PasswordConditions


class NewPasswordUI:
    '''
    Show widgets to enter New Password when user clicks reset button after
    providing credentials.
    '''

    def __init__(self, username, master, ForgotPasswordFrame, LoginFrame, RightFrame, InnerRightFrame):
        '''
        param:
            username                : Name of User
            master                  : Object of Tk
            ForgotPasswordFrame     : Frame to place all widgets in ForgotPassword UI
            LoginFrame              : Frame to place all widget in Login UI
            RightFrame              : Right Frame in ForgotPassword.py tok keep widgets in right side
            InnerRightFrame         : Frame to keep the widgets kept in RightFrame
        '''

        self.bg = '#aaff00'
        self.Assets = Assets()

        self.master = master
        self.username = username
        self.LoginFrame = LoginFrame
        self.RightFrame = RightFrame
        self.InnerRightFrame = InnerRightFrame
        self.ForgotPasswordFrame = ForgotPasswordFrame

    def ShowWidgets(self):
        '''
        Showing corresponding widgets
        '''

        self.InnerRightFrame.pack_forget()
        self.master.title('Nepal Stock Tracker | New Password')

        self.NewPasswordFrame = Frame(self.RightFrame, bg=self.bg)
        self.NewPasswordFrame.pack(pady=50)

        self.PassFrame = Frame(self.NewPasswordFrame, bg=self.bg)
        self.PassFrame.pack()
        self.PasswordEntry = _Password_Entry(self.PassFrame, 'New Password', self.bg, 40)
        self.PasswordEntry.PasswordFrame.pack()

        self.ConfirmPassFrame = Frame(self.NewPasswordFrame, bg=self.bg)
        self.ConfirmPassFrame.pack()
        self.ConfirmPasswordEntry = _Password_Entry(self.ConfirmPassFrame, 'Confirm Password', self.bg, 40)
        self.ConfirmPasswordEntry.PasswordFrame.pack(pady=10)

        self.PasswordHints = PasswordConditions(self.master, self.PassFrame, self.PasswordEntry.PasswordEntry, self.ConfirmPasswordEntry.PasswordEntry, self.ConfirmPassFrame, self.bg, 'black')

        self.SubmitButton = Button(self.NewPasswordFrame, image=self.Assets.ConfirmImage, bg=self.bg, activebackground=self.bg, bd='0', cursor='hand2', font=Font(size=10, weight='bold'), command=self.SubmitButtonCommand)
        self.SubmitButton.pack(pady=(0, 15), ipady=10)

        self.BackButton = Button(self.NewPasswordFrame, image=self.Assets.BackImage, bd=0, cursor='hand2', bg=self.bg, activebackground=self.bg, command=self.BackButtonCommand)
        self.BackButton.image = self.Assets.BackImage
        self.BackButton.pack()

        self.PasswordEntry.PasswordEntry.Entry.bind('<Return>', self.SubmitButtonCommand)
        self.ConfirmPasswordEntry.PasswordEntry.Entry.bind('<Return>', self.SubmitButtonCommand)

    def SubmitButtonCommand(self, event=None):
        '''
        Notify user that his/her password has been changed and send them to
        login page.
        '''

        PasswordDefault = self.PasswordEntry.PasswordEntry.IsDefault
        ConfirmPasswordDefault = self.ConfirmPasswordEntry.PasswordEntry.IsDefault

        Password = self.PasswordEntry.PasswordEntry.var.get().strip().strip()
        ConfirmPassword = self.ConfirmPasswordEntry.PasswordEntry.var.get().strip()

        if any([PasswordDefault, ConfirmPasswordDefault]):
            messagebox.showerror('ERR', 'Provide new password')

        elif Password != ConfirmPassword:
            messagebox.showerror('ERR', 'Provide same passwords')

        elif self.PasswordHints.IsPasswordStrong is False:
            messagebox.showerror('ERR', 'Password does not meet requirements')

        else:
            DB().ResetPassword(self.username, Password)

            messagebox.showinfo('Success', 'You password has been changed!!!\n\nNow you can login')
            self.master.title('Nepal Stock Tracker | LOGIN')

            self.ForgotPasswordFrame.destroy()
            self.LoginFrame.pack()

    def BackButtonCommand(self):
        '''
        When user clicks back button
        '''

        self.NewPasswordFrame.destroy()
        self.InnerRightFrame.pack()
        self.master.title('Nepal Stock Tracker | Change Password')
