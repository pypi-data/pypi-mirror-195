import hashlib
from tkinter import *
from tkinter.font import Font
from tkinter import messagebox

try:  # When used as a package
    from NepalStockTracker.db import DB
    from NepalStockTracker import Include
    from NepalStockTracker.Assets import Assets
    from NepalStockTracker.DashBoard import DashBoard
    from NepalStockTracker._Entry import _Entry, _Password_Entry
    from NepalStockTracker.ForgotPassword import ForgotPasswordUI

except ImportError:  # When used as a normal script
    import Include
    from db import DB
    from Assets import Assets
    from DashBoard import DashBoard
    from _Entry import _Entry, _Password_Entry
    from ForgotPassword import ForgotPasswordUI


class LoginUI:
    '''
    Show widgets for login
    '''

    def __init__(self, master, MainFrame, LOGIN, ComboValues, search):
        '''
        param:
            master          : Object to TK
            MainFrame       : Frame to keep widgets
            LOGIN           : Object of _LOGIN._LOGIN to make login
            ComboValues     : Values for comboBox
            search          : Object of Search.Search to search company
        '''

        self.bg = '#cbd0d6'
        self.LOGIN = LOGIN
        self.SEARCH = search
        self.master = master
        self.Assets = Assets()
        self.RightBG = '#6847ae'
        self.MainFrame = MainFrame
        self.IsPasswordHidden = True
        self.ComboValues = ComboValues

    def ShowWidgets(self):
        '''
        Show corresponding widgets
        '''

        if self.LOGIN.username is None:
            self.master.withdraw()
            self.MainFrame.pack_forget()
            self.master.title('Nepal Stock Tracker | LOGIN')

            self.LoginFrame = Frame(self.master, bg=self.RightBG)
            self.LoginFrame.pack()

            self.LeftFrame = Frame(self.LoginFrame)
            self.LeftFrame.pack(side=LEFT, expand=TRUE)
            self.RightFrame = Frame(self.LoginFrame, bg=self.RightBG)
            self.RightFrame.pack(side=RIGHT, anchor=CENTER)

            self.LeftLabel = Label(self.LeftFrame, image=self.Assets.LoginFrameImage, bg='#6847ae')
            self.LeftLabel.pack(ipadx=20, ipady=20)
            self.UsernameEntry = _Entry(self.RightFrame, 'Username', width=40, bg=self.RightBG)
            self.UsernameEntry.Frame.pack(ipady=5, pady=10)

            self.PasswordEntry = _Password_Entry(self.RightFrame, 'Password', self.RightBG, 40)
            self.PasswordEntry.PasswordFrame.pack(padx=(48, 0))

            self.SubmitButton = Button(self.RightFrame, imag=self.Assets.LoginButtonImage, bg=self.RightBG, activebackground=self.RightBG, activeforeground="white", bd='0', cursor='hand2', font=Font(size=10, weight='bold'), command=self.SubmitButtonCommand)
            self.SubmitButton.pack(pady=15, ipady=5)

            self.ForgotPasswordLabel = Label(self.RightFrame, text='Forgot Password ?', fg='white', bg=self.RightBG, cursor='hand2', font=Font(size=10, underline=True))
            self.ForgotPasswordLabel.pack(padx=(0, 45), pady=(10, 10), anchor='e')

            self.BackButton = Button(self.RightFrame, image=self.Assets.BackImage, bd=0, cursor='hand2', bg=self.RightBG, activebackground=self.RightBG, command=self.BackButtonCommand)
            self.BackButton.pack(pady=(30, 0))

            self.ForgotPassword = ForgotPasswordUI(self.master, self.LoginFrame)
            self.ForgotPasswordLabel.bind('<Button-1>', self.ForgotPassword.ShowWidgets)

            Include.SetWindowPosition(self.master)

            self.UsernameEntry.Entry.bind('<Return>', self.SubmitButtonCommand)
            self.PasswordEntry.PasswordEntry.Entry.bind('<Return>', self.SubmitButtonCommand)

        else:
            self.Dashboard = DashBoard(self.master, self.ComboValues, self.LOGIN, self.MainFrame, self.SEARCH)
            self.Dashboard.ShowWidgets()

    def SubmitButtonCommand(self, event=None):
        '''
        When user clicks login button after enter credentials
        '''

        UserNameDefault = self.UsernameEntry.IsDefault
        PasswordDefault = self.PasswordEntry.PasswordEntry.IsDefault

        username = self.UsernameEntry.var.get().strip()
        password = self.PasswordEntry.PasswordEntry.var.get().strip()

        if any([UserNameDefault, PasswordDefault]):
            messagebox.showerror('ERR', 'Provide valid values')
            return

        if DB().Login(username, password):
            self.UsernameEntry.SetToDefault()
            self.PasswordEntry.PasswordEntry.SetToDefault()

            self.LOGIN.login(hashlib.sha256(username.encode()).hexdigest())

            self.Dashboard = DashBoard(self.master, self.ComboValues, self.LOGIN, self.LoginFrame, self.SEARCH, self.MainFrame)
            self.Dashboard.ShowWidgets()

        else:
            messagebox.showerror('ERR', 'Username or password did not match')

    def BackButtonCommand(self):
        '''
        Go back to homepage when user clicks back button
        '''

        self.master.title('Nepal Stock Tracker')

        self.LoginFrame.destroy()
        self.MainFrame.pack(padx=50, pady=50)
