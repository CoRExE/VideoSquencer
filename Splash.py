from tkinter import *
from PIL import Image, ImageTk


class SplashScreen:
    def __init__(self, master):
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
        self.master.destroy()


splash_root = Tk()
splash = SplashScreen(splash_root)
splash_root.mainloop()
