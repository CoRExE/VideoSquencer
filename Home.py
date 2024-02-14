import os
from time import sleep
from tkinter import *
from tkinter import ttk
from libs import *
import tkinter.messagebox as messagebox

video_extension = ["mp4", "mov", "mkv", "avi", "webm", "mp3", "wav", "flv"]

process_num = os.cpu_count()
sources_path = []
dest_path = ""


# # # Interface # # #
class Home:
    def __init__(self):
        self.root = Tk()
        self.root.title("VideoSquencer")
        self.root.geometry("720x480")
        self.root.minsize(480, 320)
        self.root.iconbitmap(r"assets/VideoSquencerIcon.ico")
        self.root.config(bg='#856ff8')

        # Frames #
        self.window = Frame(self.root, cursor="crosshair", bg=self.root['bg'])
        self.path_frame = Frame(self.window, bg=self.root['bg'])
        self.liste_frame = Frame(self.window, bg=self.root['bg'])

        # Options #
        Label(self.path_frame, text="Frames", bg=self.root['bg']).pack(side="top")
        self.frame_menu = ttk.Combobox(self.path_frame, state="readonly", width=10,
                                       values=["25", "50", "75", "100", "all"])
        self.frame_menu.pack(side="top", expand=True)

        Label(self.path_frame, text="Number of process", bg=self.root['bg']).pack(side="bottom")
        self.spin_process = Spinbox(self.path_frame, from_=1, to=process_num, width=10, state="readonly")
        self.spin_process.pack(side="bottom", expand=True)

        Button(self.root, text="Launch", command=self.launch).pack(side="bottom")

        # Source #
        self.source_button = Button(self.liste_frame, text="Select Source", command=self.select_source)
        self.folder_button = Button(self.liste_frame, text="Select Folder", command=self.select_folder)
        Label(self.liste_frame, text="Fichier(s)", bg=self.root['bg']).pack(side="top")
        self.listbox = Listbox(self.liste_frame, activestyle="dotbox", bg="lightgrey", fg="black", width=50,
                               state="disabled")
        Button(self.liste_frame, text="Clear List", command=self.clear_listebox).pack(side="bottom", expand=True)

        # Dest #
        Label(self.liste_frame, text="Destination", bg=self.root['bg']).pack(side="bottom")
        self.dest_button = Button(self.liste_frame, text="Select Destination", command=self.select_dest)
        self.dest_entry = Entry(self.liste_frame, state="disabled", width=50, justify="center")

        # Pack #
        self.source_button.pack(side="left")
        self.folder_button.pack(side="right")
        self.listbox.pack(fill="both", expand=True)
        self.dest_entry.pack(side="bottom")
        self.dest_button.pack(side="bottom")

        self.path_frame.pack(expand=True, side="left")
        self.liste_frame.pack(expand=True, side="right")
        self.window.pack(expand=True, fill='both')

        self.root.mainloop()

    # Functions #

    def select_source(self):
        result = get_file_name(multiple=True)
        if type(result) == tuple:
            self.listbox.configure(state="normal")
            for source in result:
                self.listbox.insert("end", source)
            self.listbox.configure(state="disabled")
            self.check_source()
        else:
            messagebox.showwarning("File are missing", "No source selected")

    def check_source(self):
        self.listbox.configure(state="normal")
        all_sources = self.listbox.get(0, "end")
        for i, source in enumerate(all_sources):
            if source.split(".")[-1] in video_extension:
                sources_path.append(source)
        self.listbox.delete(0, "end")
        if len(sources_path) == 0:
            messagebox.showwarning("No Video Selected", "Seems like no video selected \n Please select a video file")
        else:
            for source in sources_path:
                self.listbox.insert("end", source)
        self.listbox.configure(state="disabled")

    def select_folder(self):
        target = get_directory()
        if target != "":
            for chemin_dossier, sous_dossiers, fichiers in os.walk(target):
                for nom_fichier in fichiers:
                    fichier = chemin_dossier + "/" + nom_fichier
                    if fichier.split(".")[-1] in video_extension:
                        sources_path.append(fichier)
            if len(sources_path) == 0:
                messagebox.showwarning("No Video Selected",
                                       "Seems like no video selected \n Please select a video file")
            else:
                self.listbox.configure(state="normal")
                for source in sources_path:
                    self.listbox.insert("end", source)
                self.listbox.configure(state="disabled")
        else:
            messagebox.showwarning("No destination selected", "Please select a Folder -_-")

    def select_dest(self):
        global dest_path
        result = get_directory()
        if result != "":
            dest_path = result
            self.dest_entry.configure(state="normal")
            self.dest_entry.delete(0, "end")
            self.dest_entry.insert("end", dest_path)
            self.dest_entry.configure(state="disabled")
        else:
            messagebox.showwarning("No destination selected", "Please select a destination :<")

    def clear_listebox(self):
        self.listbox.configure(state="normal")
        self.listbox.delete(0, "end")
        self.listbox.configure(state="disabled")
        sources_path.clear()

    def launch(self):
        all_sources = self.listbox.get(0, "end")
        frame_num = self.frame_menu.get()
        num_process = int(self.spin_process.get())
        if frame_num != 'all':
            frame_num = int(frame_num)
        self.root.withdraw()
        run(all_sources, self.dest_entry.get(), frame_num, num_process)
        self.root.deiconify()


def run(sources, dest_path, frame_num, num_process):
    for source in sources:
        dest_path_temp = dest_path + "/" + source.split("/")[-1].split(".")[0]
        if not os.path.exists(dest_path_temp):
            os.mkdir(dest_path_temp)
        execute(source, dest_path_temp, frame_num, num_process)
    messagebox.showinfo("Done", "All process are done")
