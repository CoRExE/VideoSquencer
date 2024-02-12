from tkinter import *
from libs import *

source_path = ""
sources_path = []
dest_path = ""


# Functions #

def select_source():
    pass


def select_dest():
    pass


### Interface ###

root = Tk()
root.title("VideoSquencer")
root.geometry("720x480")
root.minsize(480, 320)
# root.iconbitmap(r"Icon.ico")
root.config(bg='#856ff8')

# Frames #
window = Frame(root, cursor="crosshair", bg=root['bg'])
path_frame = Frame(window, bg=root['bg'])

# Sources #
sources_label = Label(window, text="Source(s)")
sources_entry = Entry(window, width=50, bg="lightgrey", fg="black", state="readonly")
source_button = Button(window, text="Select Source", command=select_source)

# Dest #
# TODO !!!


# Pack #
sources_label.pack()
sources_entry.pack()
source_button.pack()

path_frame.pack(expand=True, fill='both', side="left")
window.pack(expand=True, fill='both')

root.mainloop()
