from tkinter import *
import tkinter.ttk as ttk
from tkinter.font import Font
import requests

try:  # When used as a package
    from NepalStockTracker import Search
    from NepalStockTracker import Include
    from NepalStockTracker.Assets import Assets
    from NepalStockTracker._Login import _Login
    from NepalStockTracker.LoginUI import LoginUI
    from NepalStockTracker.SignUpUI import SignUpUI
    from NepalStockTracker._ComboBox import _ComboBox
    from NepalStockTracker.PlayErrorAudio import Play

except ImportError:  # When used as a normal script
    import Search
    import Include
    from Assets import Assets
    from _Login import _Login
    from LoginUI import LoginUI
    from SignUpUI import SignUpUI
    from _ComboBox import _ComboBox
    from PlayErrorAudio import Play


__all__ = ['StockTracker']


class StockTracker:
    def __init__(self, CompanySymbol='', ShowGUI=True):
        '''
        param:
            CompanySymbol  : abbreviation of company name
            ShowGUI        : True | False
        '''

        if ShowGUI:
            self.LOGIN = _Login()

            self.StartTimer = 0
            self.ErrorTimer = None
            self.PreviousSearch = ''
            self.FrontColor = '#cdfa05'
            self.DetailsFrameDeleted = False
            self.DEFAULTTEXT = 'COMPANY SYMBOL'

            self.master = Tk()
            self.Assets = Assets()
            self.master.withdraw()
            self.master.title('Nepal Stock Tracker')
            self.master.iconphoto(False, self.Assets.IconImage)
            self.SEARCH = Search.Search(self.ShowErrorMessage, self.CheckInternet, master=self.master)

            self.master.config(bg=self.FrontColor)
            self.OptionValues = self.SEARCH.GetCompaniesNameList()
            self.OptionValues.sort()

            self.MainFrame = Frame(self.master, bg=self.FrontColor)
            self.MainFrame.pack(padx=50, pady=50)

            self.WidgetsFrame = Frame(self.MainFrame, bg=self.FrontColor)
            self.WidgetsFrame.pack(side=LEFT)

            self.TitleLabel = Label(self.WidgetsFrame, image=self.Assets.TitleImage, bg=self.FrontColor)
            self.TitleLabel.pack()

            self.CompanyName = _ComboBox(self.master, self.WidgetsFrame, self.OptionValues)
            self.CompanyName.ComboBox.pack(pady=10, ipady=3)

            self.DataButton = Button(self.WidgetsFrame, text="Get Company Details", width=33, fg='white', bg="#006837", activebackground="#006837", activeforeground="white", bd='0', cursor='hand2', font=Font(size=10, weight='bold'), command=self.ShowMarketDetails)
            self.DataButton.pack(ipady=8)

            self.Login = LoginUI(self.master, self.MainFrame, self.LOGIN, self.OptionValues, self.SEARCH)
            self.LoginButton = Button(self.WidgetsFrame, text="LOGIN", width=33, fg='white', bg="#006837", activebackground="#006837", activeforeground="white", bd='0', cursor='hand2', font=Font(size=10, weight='bold'), command=self.Login.ShowWidgets)
            self.LoginButton.pack(pady=10, ipady=8)

            self.SignUp = SignUpUI(self.master, self.MainFrame, self.Login, self.FrontColor)
            self.SignUpLabelFrame = Frame(self.WidgetsFrame, bg=self.FrontColor)
            self.SignUpLabelFrame.pack(fill='x', pady=(10, 0), padx=(0, 18))
            self.SignUpLabelLabel = Label(self.SignUpLabelFrame, text='Don\'t have an account?', fg='#211a17', bg=self.FrontColor, bd=0, font=Font(size=10, underline=True), cursor='hand2')
            self.SignUpLabelLabel.pack(side=RIGHT)

            self.DetailsFrame = Frame(self.MainFrame, bg=self.FrontColor)
            self.DetailsFrame.pack(pady=(10, 0), padx=(30, 0), side=RIGHT)

            Include.SetWindowPosition(self.master)

            self.master.bind('<Control-r>', self.Retry)
            self.master.bind('<Button-1>', self.ChangeFocus)
            self.master.bind_all('<F5>', self.ShowMarketDetails)
            self.CompanyName.ComboBox.bind('<Return>', self.ShowMarketDetails)
            self.SignUpLabelLabel.bind('<Button-1>', self.SignUp.ShowWidgets)

            self.master.mainloop()

        else:
            self.SEARCH = Search.Search(self.ShowErrorMessage, self.CheckInternet)
            self.details = self.SEARCH.get_data(CompanySymbol)

    def Retry(self, event=None):
        '''
        Retry to get the company names if not retrieved at first
        '''

        if self.CheckInternet():
            self.OptionValues = self.SEARCH.GetCompaniesNameList()
            self.CompanyName.ComboBox.set(self.DEFAULTTEXT)
            self.CompanyName.ComboBox.config(values=self.OptionValues)
            self.ShowErrorMessage('Retrieved Company Names successfully')

        else:
            self.ShowErrorMessage('Failed to get Company Names. No Internet.\nPress Control + R to retry.', _time=5000)

    def CheckInternet(self):
        '''
        Check if the user is connected to internet
        '''

        try:
            requests.get('https://google.com')
            return True

        except requests.ConnectionError:
            return False

    def ChangeFocus(self, event=None):
        '''
        Change focus to the respective widget where user has clicked
        '''

        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)

        if not isinstance(widget, (ttk.Combobox, type(None))):
            widget.focus_set()

    def ShowMarketDetails(self, event=None):
        '''
        Display company details if available
        '''

        for child in self.DetailsFrame.winfo_children():  # Destroying all widgets inside of self.DetailsFrame
            child.destroy()

        ErrorMessage = ''
        value = self.CompanyName.ComboVar.get().strip()

        if '(' in value:
            value = value[:value.index('(')]

        # Fonts for the extracted values
        label_font = Font(size=10, weight='bold')
        font1, font2 = Font(size=15), Font(size=10)

        if value and value != self.DEFAULTTEXT:
            if self.CheckInternet():
                details = self.SEARCH.get_data(value)

                sector = details['sector']
                change = details['change']
                HighLow = details['high_low']
                date = details['last_traded_on']
                AverageValue = details['average']
                ShareValue = details['market_price']
                CompanyName = details['company_name']

                if self.DetailsFrameDeleted:
                    self.DetailsFrameDeleted = False
                    self.DetailsFrame.pack(pady=(10, 0), padx=(30, 0), side=RIGHT)

                self.CompanyNameFrame = Frame(self.DetailsFrame, bg=self.FrontColor)
                self.CompanyNameFrame.pack()

                CompanyNameLabel = Label(self.CompanyNameFrame, text=CompanyName, font=font1, fg='green', wraplength=250, bg=self.FrontColor)
                CompanyNameLabel.pack(side=LEFT, pady=(10, 20), padx=(0, 30))

                self.RemoveButton = Button(self.CompanyNameFrame, image=self.Assets.DeleteImage, bd=0, anchor='e', bg=self.FrontColor, activebackground=self.FrontColor, command=self.DeleteCommand)
                self.RemoveButton.pack(side=RIGHT)

                # Displaying sector details
                SectorFrame = Frame(self.DetailsFrame, bg=self.FrontColor)
                SectorFrame.pack(fill='x')
                SectorLabel = Label(SectorFrame, text="Sector", fg="#333333", font=label_font, bg=self.FrontColor)
                SectorLabel.pack(side=LEFT)
                SectorName = Label(SectorFrame, text=sector, fg='#1c8b98', font=font2, bg=self.FrontColor)
                SectorName.pack(side=RIGHT)

                # Displaying current stock value of the company
                MarketPriceFrame = Frame(self.DetailsFrame, bg=self.FrontColor)
                MarketPriceFrame.pack(fill='x')
                MarketLabel = Label(MarketPriceFrame, text='Market Price', fg="#333333", font=label_font, bg=self.FrontColor)
                MarketLabel.pack(side=LEFT)
                MarketPrice = Label(MarketPriceFrame, text=ShareValue, font=Font(size=10, weight='bold'), bg=self.FrontColor)
                MarketPrice.pack(side=RIGHT)

                # Displaying change percentage
                ChangeFrame = Frame(self.DetailsFrame, bg=self.FrontColor)
                ChangeFrame.pack(fill='x')
                ChangeLabel = Label(ChangeFrame, text='% Change', fg="#333333", font=label_font, bg=self.FrontColor)
                ChangeLabel.pack(side=LEFT)
                ChangeValue = Label(ChangeFrame, text=change, font=font2, bg=self.FrontColor)
                ChangeValue.pack(side=RIGHT)

                # Displaying last trade date of the company
                LastTradeFrame = Frame(self.DetailsFrame, bg=self.FrontColor)
                LastTradeFrame.pack(fill='x')
                LastTradeDateLabel = Label(LastTradeFrame, text='Last Traded On', fg="#333333", font=label_font, bg=self.FrontColor)
                LastTradeDateLabel.pack(side=LEFT)
                LastTradeDate = Label(LastTradeFrame, text=date, width=20, anchor='e', font=font2, bg=self.FrontColor)
                LastTradeDate.pack(side=RIGHT)

                # Displaying high and low price of the company
                HighLowFrame = Frame(self.DetailsFrame, bg=self.FrontColor)
                HighLowFrame.pack(fill='x')
                HighLowLabel = Label(HighLowFrame, text='High-Low', fg="#333333", font=label_font, bg=self.FrontColor)
                HighLowLabel.pack(side=LEFT)
                HighLowLabelValue = Label(HighLowFrame, text=HighLow, width=20, anchor='e', font=font2, bg=self.FrontColor)
                HighLowLabelValue.pack(side=RIGHT)

                # Displaying company's average market value of the company
                AverageFrame = Frame(self.DetailsFrame, bg=self.FrontColor)
                AverageFrame.pack(fill='x')
                AverageLabel = Label(AverageFrame, text='120 Day Average', fg="#333333", font=label_font, bg=self.FrontColor)
                AverageLabel.pack(side=LEFT)
                AverageLabelValue = Label(AverageFrame, text=AverageValue, width=20, anchor='e', font=font2, bg=self.FrontColor)
                AverageLabelValue.pack(side=RIGHT)

                if (ShareValue, change, date, HighLow, AverageValue) == ('0.00', '0 %', '', '0.00-0.00', '0.00'):
                    color = '#ff3333'

                else:
                    changed = self.SEARCH.Profit_Loss_Or_Neutral(value)

                    if change == '0 %':  # When company stock price has not been changed
                        color = '#ed9c28'

                    elif 'decrease' in changed:  # When company stock price has been decreased
                        color = '#ff3333'

                    else:  # When company stock price has been increased
                        color = '#0dbe0d'

                MarketPrice.config(fg=color)
                ChangeValue.config(fg=color)

                self.master.update()

            else:
                # When user is not connected to internet
                ErrorMessage = 'No Internet Connection'

        else:
            # When user tries to get company market details without
            # inserting any company in the entry widget
            ErrorMessage = 'Invalid Company Symbol'

        if ErrorMessage:
            self.ShowErrorMessage(ErrorMessage)

    def ShowErrorMessage(self, ErrorMessage, _time=1500):
        '''
        Show error message when there is no internet and when user does not
        provide any company name

        param:
            ErrorMessage  : The actual error message to display
            _time          : For long should the error message be displayed(in ms)
        '''

        if self.ErrorTimer is None:
            for child in self.DetailsFrame.winfo_children():
                child.destroy()

            Play()

            ErrorMessageVar = StringVar()
            ErrorMessageVar.set(ErrorMessage)

            label = Label(self.DetailsFrame, textvariable=ErrorMessageVar, fg='red', font=Font(size=10, weight='bold'), bg=self.FrontColor)
            label.pack()
            self.ErrorTimer = self.master.after(_time, lambda: self.RemoveErrorMessage(label))

        else:
            self.master.after_cancel(self.ErrorTimer)
            self.ErrorTimer = None
            self.master.after(0, lambda: self.ShowErrorMessage(ErrorMessage, _time))

    def RemoveErrorMessage(self, lbl):
        '''
        Destroy the error message

        param:
            lbl : Label object

        '''

        lbl.destroy()
        temp_frame = Frame(self.DetailsFrame, width=1, height=1)
        temp_frame.pack()
        self.master.update_idletasks()
        temp_frame.destroy()

        self.ErrorTimer = None

    def DeleteCommand(self):
        '''
        Remove details frame
        '''

        self.DetailsFrameDeleted = True
        self.DetailsFrame.pack_forget()


if __name__ == '__main__':
    StockTracker()
