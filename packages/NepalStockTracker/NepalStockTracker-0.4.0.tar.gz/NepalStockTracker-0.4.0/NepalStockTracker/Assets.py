import sys
from tkinter import PhotoImage
from PIL import Image as IMG, ImageTk

try:  # When used as a package
    from NepalStockTracker import Include

except ImportError:  # When used as a normal script
    import Include


class Assets:
    '''
    PhotoImage object to reduce code redundancy
    '''

    def __init__(self):
        if sys.platform == 'win32':
            self.ErrorAudio = Include.ResourcePath('WinErrSound.wav')

        else:
            self.ErrorAudio = Include.ResourcePath('LinuxErrSound.wav')

        self.DeleteImage = Include.ResourcePath('Delete.png')
        self.DeleteImage = IMG.open(self.DeleteImage)
        self.DeleteImage.thumbnail((20, 20), IMG.Resampling.LANCZOS)
        self.DeleteImage = ImageTk.PhotoImage(self.DeleteImage)

        self.TickImage = Include.ResourcePath('Tick.png')
        self.TickImage = IMG.open(self.TickImage)
        self.TickImage.thumbnail((15, 15), IMG.Resampling.LANCZOS)
        self.TickImage = ImageTk.PhotoImage(self.TickImage)

        self.AddImage = PhotoImage(file=Include.ResourcePath('Add.png'))
        self.IconImage = PhotoImage(file=Include.ResourcePath('icon.png'))
        self.BackImage = PhotoImage(file=Include.ResourcePath('Back.png'))
        self.ResetImage = PhotoImage(file=Include.ResourcePath('Reset.png'))
        self.SubmitImage = PhotoImage(file=Include.ResourcePath('Submit.png'))
        self.LogoutImage = PhotoImage(file=Include.ResourcePath('Logout.png'))
        self.ConfirmImage = PhotoImage(file=Include.ResourcePath('Confirm.png'))
        self.TitleImage = PhotoImage(file=Include.ResourcePath('Title Image.png'))
        self.LoginButtonImage = PhotoImage(file=Include.ResourcePath('Login.png'))
        self.LoginFrameImage = PhotoImage(file=Include.ResourcePath('Login Frame.png'))
        self.SignUpFrameImage = PhotoImage(file=Include.ResourcePath('Signup Frame.png'))
        self.DashBoardImage = PhotoImage(file=Include.ResourcePath('DashBoard Frame.png'))
        self.HidePasswordImage = PhotoImage(file=Include.ResourcePath('Hide Password.png'))
        self.ShowPasswordImage = PhotoImage(file=Include.ResourcePath('Show Password.png'))
        self.ForgotPasswordFrameImage = PhotoImage(file=Include.ResourcePath('Forgot Password Frame.png'))
