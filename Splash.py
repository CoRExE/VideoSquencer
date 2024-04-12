from tkinter import Label
from PIL import Image, ImageTk


class SplashScreen:
    def __init__(self, master):
        """
        Initialize the splash screen window with a given master window.
        Set the window to be borderless, with a specific size and position.
        Load an image to display on the window.
        Create a label and add the image to it.
        Close the splash screen window after 5 seconds.
        """
        self.master = master
        self.master.overrideredirect(True)
        self.master.geometry('500x500+300+300')  # Set the window size and position

        # Load the image
        self.image = Image.open(r"./assets/VideoSquencerIconResized.png")
        self.photo_image = ImageTk.PhotoImage(self.image)

        # Create a label and add the image to it
        self.label = Label(self.master, image=self.photo_image)
        self.label.pack()

        # Close the splash screen after 5 seconds
        self.master.after(5000, self.close_splash)

    def close_splash(self):
        """
        Closes the splash screen by destroying the master window.
        """
        self.master.destroy()

