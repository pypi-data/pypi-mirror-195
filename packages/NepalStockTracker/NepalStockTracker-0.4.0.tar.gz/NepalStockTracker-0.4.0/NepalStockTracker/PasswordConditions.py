import string
from tkinter import *
from tkinter.font import Font

try:
    from NepalStockTracker.Assets import Assets

except ImportError:
    from Assets import Assets


class PasswordConditions:
    def __init__(self, master, frame, entry, ReEntry, PasswordMatchedFrame, bg, fg='white'):
        self.RightBG = bg
        self.Entry = entry
        self.master = master
        self.EntryVar = entry
        self.Assets = Assets()
        self.ReEntry = ReEntry
        self.IsPasswordStrong = False
        self.PasswordMatchedFrame = PasswordMatchedFrame

        self.PasswordConditions = [
                "● length is at least 8",
                "● contains digit",
                "● contains lowercase",
                "● contains uppercase",
                "● contains special character: !@#$%^&*()-+"
        ]

        self.Frame = Frame(frame, bg=self.RightBG)
        self.Frame.pack()

        self.PasswordMatchedLabelFrame = Frame(self.PasswordMatchedFrame, bg=self.RightBG)
        self.PasswordMatchedLabel = Label(self.PasswordMatchedLabelFrame, bg=self.RightBG)
        self.PasswordMatchedLabel.pack()

        self.TickImage = self.Assets.TickImage

        self.RespectiveWidgets = dict()
        checked_values = ['8', 'digit', 'lowercase', 'uppercase', 'special']

        # Placing conditions labels
        for index, item in enumerate(self.PasswordConditions):
            frame = Frame(self.Frame)
            frame.pack()

            image_label = Label(frame, bg=self.RightBG, fg=fg, width=40, text=item, compound='left', anchor='w')
            image_label.pack(side=LEFT)

            self.RespectiveWidgets[checked_values[index]] = image_label

        self.ReEntry.var.trace('w', self.CheckForPasswordMatch)
        self.Entry.var.trace('w', self.CheckForConditionVerification)

    def CheckForConditionVerification(self, *args):
        '''
        When any changes is made in first password widget
        '''

        if self.Entry.IsDefault is False:
            values = self.Entry.var.get()
            self.AddRemoveTickImage(values)

    def CheckForPasswordMatch(self, *args):
        '''
        Display Password Matched label for 1500ms
        '''

        if self.Entry.IsDefault is False:
            if self.Entry.IsDefault is False:
                FirstPassword = self.Entry.var.get().strip()
                AnotherPassword = self.ReEntry.var.get().strip()

                if FirstPassword == AnotherPassword:
                    self.PasswordMatchedLabel.config(text='Password matched', fg='dark green', font=Font(size=12, weight='bold'))
                    self.PasswordMatchedLabelFrame.pack(pady=(0, 10))

                    self.master.after(1500, self.PasswordMatchedLabelFrame.pack_forget)

    def CheckForStrongPassword(self, password):
        '''
        Check if user have entered the strong password

        param:
            password    : Text entered in password-widget
        '''

        length = len(password)

        hasLower = False
        hasUpper = False
        hasDigit = False
        hasSpecialChar = False
        hasLengthMoreThanEight = False

        if length >= 8:
            hasLengthMoreThanEight = True

        for i in range(length):
            if password[i] in string.ascii_lowercase:
                hasLower = True

            elif password[i] in string.ascii_uppercase:
                hasUpper = True

            elif password[i] in string.digits:
                hasDigit = True

            elif password[i] in string.punctuation:
                hasSpecialChar = True

        return [hasLengthMoreThanEight, hasDigit, hasLower, hasUpper, hasSpecialChar]

    def AddRemoveTickImage(self, text):
        '''
        Replace ● with tick image when the respective password conditions gets
        satisfied
        '''

        self.IsPasswordStrong = self.CheckForStrongPassword(text)

        for index, value in enumerate(self.RespectiveWidgets.values()):
            if self.IsPasswordStrong[index]:
                if value.cget('image') == '':
                    value.config(image=self.TickImage, text=value.cget('text')[1:], width=280)
                    value.image = self.TickImage

                    self.master.update()

            elif value.cget('image'):
                value.config(image='', text=f"● {value.cget('text').strip()}", width=40)
                value.image = ''

        if all(self.IsPasswordStrong):
            self.IsPasswordStrong = True
            self.Frame.pack_forget()

        elif self.IsPasswordStrong:
            self.IsPasswordStrong = False
            self.Frame.pack()
