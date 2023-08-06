import datetime
import threading
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox

try:  # When used as a package
    from NepalStockTracker.db import DB
    from NepalStockTracker import exceptions
    from NepalStockTracker.Assets import Assets
    from NepalStockTracker._ComboBox import _ComboBox

except ImportError:  # When used as a normal script
    import exceptions
    from db import DB
    from Assets import Assets
    from _ComboBox import _ComboBox


class DashBoard:
    '''
    Show the information of respective user when user logs in successfully
    '''

    def __init__(self, master, ComboValues, LOGIN, MainFrame, search, DestroyedMainFrame=None):
        '''
        param:
            master              : Object of Tk
            ComboValues         : Values for ComboBox
            LOGIN               : Object of _Login._Login
            MainFrame           : Frame to keep widgets
            search              : Object of Search.Search
            DestroyedMainFrame  : None | True | False
                                  If none then root window has been destroyed
        '''

        self.sn = 0
        self.LOGIN = LOGIN
        self.master = master
        self.PrevHash = None
        self.Assets = Assets()
        self.RightBG = '#a4f5ec'
        self.MainFrame = MainFrame
        self.IsScrollBarShown = False
        self.ComboValues = ComboValues
        self.username = self.LOGIN.username
        self.DestroyedMainFrame = DestroyedMainFrame

        self.SEARCH = search
        self.EndThread = False

    def ShowWidgets(self):
        '''
        Show corresponding widgets
        '''

        self.MainFrame.pack_forget()
        self.ThreadEvent = threading.Event()
        self.master.title('Nepal Stock Tracker | DashBoard')

        self.DashboardFrame = Frame(self.master, bg=self.RightBG)
        self.DashboardFrame.pack()

        self.LeftImage = Label(self.DashboardFrame, image=self.Assets.DashBoardImage, bg='#a4f5ec')
        self.LeftImage.pack(side=LEFT)

        self.RightFrame = Frame(self.DashboardFrame, bg=self.RightBG)
        self.RightFrame.pack(side=RIGHT)

        self.ComboFrame = Frame(self.RightFrame, bg=self.RightBG)
        self.ComboFrame.pack(pady=15)

        self.combobox = _ComboBox(self.master, self.ComboFrame, self.ComboValues, width=70)
        self.combobox.ComboBox.pack(side=LEFT, ipady=3)
        self.AddButton = Button(self.ComboFrame, image=self.Assets.AddImage, bd=0, cursor='hand2', bg=self.RightBG, activebackground=self.RightBG, command=self.AddButtonCommand)
        self.AddButton.pack(side=LEFT)

        self.TreeviewFrame = Frame(self.RightFrame, bg=self.RightBG)
        self.TreeviewFrame.pack(pady=(0, 10), padx=(20, 0))
        self.TreeViewLeftFrame = Frame(self.TreeviewFrame, bg=self.RightBG)
        self.TreeViewLeftFrame.pack(side=LEFT)

        self.Treeview = ttk.Treeview(self.TreeViewLeftFrame, columns=('SN', 'Scrip', 'Sector', 'Price'), show='headings', height=15)
        self.Treeview.pack(side=LEFT)

        self.Scrollbar = ttk.Scrollbar(self.TreeViewLeftFrame, orient='vertical', command=self.Treeview.yview)
        self.LogOutButton = Button(self.TreeviewFrame, image=self.Assets.LogoutImage, bd=0, cursor='hand2', bg=self.RightBG, activebackground=self.RightBG, command=self.LogOutButtonCommand)
        self.LogOutButton.pack(side=RIGHT)

        self.BackButton = Button(self.RightFrame, image=self.Assets.BackImage, bd=0, cursor='hand2', bg=self.RightBG, activebackground=self.RightBG, command=self.BackButtonCommand)
        self.BackButton.pack(pady=(20, 10))

        self.Treeview.column('SN', width=50, anchor='center')
        self.Treeview.column('Scrip', width=100, anchor='center')
        self.Treeview.column('Price', width=100, anchor='center')
        self.Treeview.column('Sector', width=300, anchor='center')

        self.Treeview.heading('SN', text='SN')
        self.Treeview.heading('Scrip', text='Scrip')
        self.Treeview.heading('Sector', text='Sector')
        self.Treeview.heading('Price', text='Price')

        self.Treeview.bind('<Button-3>', self.RightClick)
        self.Treeview.bind('<Motion>', self.RestrictResizingHeading)
        self.Treeview.bind('<Button-1>', self.RestrictResizingHeading)
        self.combobox.ComboBox.bind('<Return>', self.AddButtonCommand)

        self.Threads = []

        for func in [self.InsertAtFirst, self.UpdateMarketPrice]:
            thread = threading.Thread(target=func)
            self.Threads.append(thread)

        for thread in self.Threads:
            thread.start()

    def RestrictResizingHeading(self, event):
        '''
        Restrict user to resize the columns of Treeview
        '''

        if self.Treeview.identify_region(event.x, event.y) == "separator":
            return "break"

    def ShowScrollBar(self):
        '''
        Show ScrollBar when the contents of TreeView is more than its height
        '''

        if self.IsScrollBarShown is False:
            self.IsScrollBarShown = True

            if self.Treeview.cget('height') < len(self.Treeview.get_children()):
                self.Scrollbar.pack(side=RIGHT, fill='y')
                self.Treeview.config(yscrollcommand=self.Scrollbar.set)

    def HideScrollBar(self):
        '''
        Hide ScrollBar when the contents of TreeView is less or equal than to
        its height
        '''

        if self.IsScrollBarShown:
            self.IsScrollBarShown = False

            if self.Treeview.cget('height') >= len(self.Treeview.get_children()):
                self.Scrollbar.pack_forget()

    def IsMarketOpen(self):
        '''
        Check if share market is open

        Nepal's share market opens from 11 am to 3 pm from Sunday to Thursday
        and from 11 am to 1 pm on Friday.
        '''

        # Getting Nepal's time when this program is ran from different time zone
        utc_time = datetime.datetime.utcnow()
        nepal_time = utc_time + datetime.timedelta(hours=5, minutes=45)
        week_day = nepal_time.weekday

        # When it is Saturday then market is closed
        if week_day == 5:
            return False

        # When it is Friday then market is opened from 11 am to 1 pm
        elif week_day == 4 and 11 <= nepal_time.hour <= 13:
            return True

        # If it is another day then market is opened from 11 am to 3 pm
        elif 11 <= nepal_time.hour <= 15:
            return True

        return False

    def UpdateMarketPrice(self):
        '''
        Update changed market_price of respective company in Treeview
        '''

        if self.EndThread is False:
            if self.IsMarketOpen():
                for child in self.Treeview.get_children():
                    thread = threading.Thread(target=self.ModifyTreeView, args=(child,), daemon=True)
                    thread.start()

            self.UpdateMarketPriceTimer = self.master.after(60000, self.UpdateMarketPrice)

    def ModifyTreeView(self, child):
        '''
        This function actually searches current market_price from the web,
        compares it with the current one present in the TreeView and changes
        the current one with the fetched one if it has been changed.

        When the search is being done, it takes a little time(like 5sec) which
        freezes the window for that about of time. To prevent this , this
        function gets called from the threading module.

        param:
            child       : Value of respective children of TreeView
        '''

        TreeViewValue = self.Treeview.item(child)['values']

        TreeViewCompanyAbbr = TreeViewValue[1]
        TreeViewValueMarketValue = TreeViewValue[-1]

        WebMarketValue = self.GetData(TreeViewCompanyAbbr)

        if WebMarketValue is not None:
            WebMarketValue = WebMarketValue[-1]

            if TreeViewValueMarketValue != WebMarketValue:
                InsertValue = TreeViewValue[:-1] + [WebMarketValue]

                self.Treeview.item(child, values=InsertValue)

    def GetData(self, company):
        '''
        Get values required to insert at TreeView

        param:
            company     : Name of Company
        '''

        try:
            details = self.SEARCH.get_data(company)
            return [company, details['sector'], details['market_price']]

        except exceptions.ConnectionError:
            return None

    def InsertAtFirst(self):
        '''
        Insert values stored in files each time when dashboard is shown
        '''

        companies = DB().GetCompanyName(self.LOGIN.username)

        for company in companies:
            try:
                self.InsertToTreeView(company)

            except RuntimeError:
                self.EndThread = True
                return

    def InsertToTreeView(self, FromComboBox):
        '''
        Insert values to the TreeView

        param:
            FromComboBox    : Company Name
        '''

        self.sn += 1
        details = self.GetData(FromComboBox)

        if details is not None:
            values = [self.sn] + details
            self.Treeview.insert('', END, values=values)

        self.ShowScrollBar()

    def AddButtonCommand(self, event=None):
        '''
        Add selected company to respective user
        '''

        FromComboBox = self.combobox.ComboVar.get().strip()

        if FromComboBox not in self.combobox.values:
            messagebox.showerror('ERR', 'Select valid company name')

        else:
            username = self.LOGIN.username
            DB().AddCompany(username, FromComboBox)

            CompanyFromTreeView = []
            FromComboBox = FromComboBox.split()[0]

            for child in self.Treeview.get_children():
                values = self.Treeview.item(child)['values'][0]

                CompanyFromTreeView.append(values)

            if FromComboBox not in CompanyFromTreeView:
                thread = threading.Thread(target=self.InsertToTreeView, args=(FromComboBox,))
                thread.start()

            self.combobox.ComboVar.set('COMPANY NAME')

    def LogOutButtonCommand(self):
        '''
        Logs out of the current logged in account
        '''

        self.LOGIN.username = None
        self.BackButtonCommand()

    def RightClick(self, event=None):
        '''
        When user right clicks inside Treeview
        '''

        CurrentSelections = self.Treeview.selection()
        RightClickMenu = Menu(self.master, tearoff=False)
        iid = self.Treeview.identify_row(event.y)

        if not CurrentSelections and not iid:
            return

        if not CurrentSelections:
            self.Treeview.selection_set(iid)

        RightClickMenu.add_command(label='Delete', activeforeground='white', activebackground='red', command=self.RightClickDelete)

        try:
            RightClickMenu.post(event.x_root, event.y_root)

        finally:
            RightClickMenu.grab_release()

    def RightClickDelete(self):
        '''
        Delete the selected company(ies) when clicked to delete option from
        right click
        '''

        CurrentSelections = self.Treeview.selection()

        if CurrentSelections:
            for selection in CurrentSelections:
                self.sn -= 1
                values = self.Treeview.item(selection)['values'][1]

                DB().RemoveCompany(values)

                self.Treeview.delete(selection)

            for idx, child in enumerate(self.Treeview.get_children()):
                index = idx + 1
                values = self.Treeview.item(child)['values']

                if values[0] != index:
                    values[0] = index
                    self.Treeview.item(child, values=values)

                self.HideScrollBar()

    def BackButtonCommand(self):
        '''
        Display homepage when user clicks back button or log-out button
        '''

        self.EndThread = True
        self.master.after_cancel(self.UpdateMarketPriceTimer)

        if self.DestroyedMainFrame is None:
            self.DestroyedMainFrame = self.MainFrame

        self.DashboardFrame.destroy()
        self.DestroyedMainFrame.pack(padx=50, pady=50)

        self.master.title('Nepal Stock Tracker')
