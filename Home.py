import os
from tkinter import *
from tkinter import ttk
from libs import *
import tkinter.messagebox as messagebox

video_extension = ["mp4", "mov", "mkv", "avi", "webm", "mp3", "wav", "flv"]

process_num = os.cpu_count()
sources_path = []
dest_path = ""


# Functions #

def select_source():
    result = get_file_name(multiple=True)
    if type(result) == tuple:
        listbox.configure(state="normal")
        for source in result:
            listbox.insert("end", source)
        listbox.configure(state="disabled")
        check_source()
    else:
        messagebox.showwarning("File are missing", "No source selected")


def check_source():
    listbox.configure(state="normal")
    all_sources = listbox.get(0, "end")
    for i, source in enumerate(all_sources):
        if source.split(".")[-1] in video_extension:
            sources_path.append(source)
    listbox.delete(0, "end")
    if len(sources_path) == 0:
        messagebox.showwarning("No Video Selected", "Seems like no video selected \n Please select a video file")
    else:
        for source in sources_path:
            listbox.insert("end", source)
    listbox.configure(state="disabled")


def select_folder():
    target = get_directory()
    if target != "":
        for chemin_dossier, sous_dossiers, fichiers in os.walk(target):
            for nom_fichier in fichiers:
                fichier = os.path.join(chemin_dossier, nom_fichier)
                if fichier.split(".")[-1] in video_extension:
                    sources_path.append(fichier)
    else:
        messagebox.showwarning("No destination selected", "Please select a destination :<")
    if len(sources_path) == 0:
        messagebox.showwarning("No Video Selected", "Seems like no video selected \n Please select a video file")
    else:
        listbox.configure(state="normal")
        for source in sources_path:
            listbox.insert("end", source)
        listbox.configure(state="disabled")


def select_dest():
    global dest_path
    result = get_directory()
    if result != "":
        dest_path = result
        dest_entry.configure(state="normal")
        dest_entry.delete(0, "end")
        dest_entry.insert("end", dest_path)
        dest_entry.configure(state="disabled")
    else:
        messagebox.showwarning("No destination selected", "Please select a destination :<")


def clear_listebox():
    listbox.configure(state="normal")
    listbox.delete(0, "end")
    listbox.configure(state="disabled")


def launch():
    all_sources = listbox.get(0, "end")
    for source in all_sources:
        dest_path_temp = dest_path + "/" + source.split("/")[-1].split(".")[0]
        os.mkdir(dest_path_temp)
        frame_num = frame_menu.get()
        if frame_menu == "all":
            frame_num = int(frame_num)
        execute(source, dest_path_temp, frame_num, int(spin_process.get()))

# # # Interface # # #

root = Tk()
root.title("VideoSquencer")
root.geometry("720x480")
root.minsize(480, 320)
root.iconbitmap(r"assets/VideoSquencerIcon.ico")
root.config(bg='#856ff8')

# Frames #
window = Frame(root, cursor="crosshair", bg=root['bg'])
path_frame = Frame(window, bg=root['bg'])
liste_frame = Frame(window, bg=root['bg'])

# Options #
Label(path_frame, text="Frames", bg=root['bg']).pack(side="top")
frame_menu = ttk.Combobox(path_frame, state="readonly", width=10, values=["25", "50", "75", "100", "all"])
frame_menu.pack(side="top", expand=True)

Label(path_frame, text="Number of process", bg=root['bg']).pack(side="bottom")
spin_process = Spinbox(path_frame, from_=1, to=process_num, width=10)
spin_process.pack(side="bottom", expand=True)

Button(root, text="Launch", command=launch).pack(side="bottom")

# Source #
source_button = Button(liste_frame, text="Select Source", command=select_source)
folder_button = Button(liste_frame, text="Select Folder", command=select_folder)
Label(liste_frame, text="Fichier(s)", bg=root['bg']).pack(side="top")
listbox = Listbox(liste_frame, activestyle="dotbox", bg="lightgrey", fg="black", width=50, state="disabled")
Button(liste_frame, text="Clear List", command=clear_listebox).pack(side="bottom", expand=True)

# Dest #
Label(liste_frame, text="Destination", bg=root['bg']).pack(side="bottom")
dest_button = Button(liste_frame, text="Select Destination", command=select_dest)
dest_entry = Entry(liste_frame, state="disabled", width=50, justify="center")

# Pack #
source_button.pack(side="left")
folder_button.pack(side="right")
listbox.pack(fill="both", expand=True)
dest_entry.pack(side="bottom")
dest_button.pack(side="bottom")

path_frame.pack(expand=True, side="left")
liste_frame.pack(expand=True, side="right")
window.pack(expand=True, fill='both')

if __name__ == "__main__":
    root.mainloop()
