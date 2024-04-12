import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from Splash import SplashScreen
from libs import execute
from libs.HTMLWriter import HTMLReportWriter
from libs.Metadata import get_metadata
from libs.Navigate import get_file_name, get_directory

video_extension = ["mp4", "avi", "webm", "mov", "mkv", "wmv", "flv", "divx", "xvid", "3gp", "mpg", "mpeg", "ts"]

process_num = os.cpu_count()
sources_path = []
dest_path = ""


# # # Interface # # #
class Home:
    def __init__(self):
        """
        Initializes the application window and sets up the necessary frames, labels, buttons, and widgets for the
        VideoSquencer application.
        """
        splash = tk.Tk()
        SplashScreen(splash)
        splash.mainloop()
        self.root = tk.Tk()
        self.root.title("VideoSquencer")
        self.root.geometry("720x480")
        self.root.minsize(480, 320)
        self.root.iconbitmap(r"./assets/VideoSquencerIcon.ico")
        self.root.config(bg='#856ff8')

        # Frames #
        self.window = tk.Frame(self.root, cursor="crosshair", bg=self.root['bg'])
        self.path_frame = tk.Frame(self.window, bg=self.root['bg'])
        self.liste_frame = tk.Frame(self.window, bg=self.root['bg'])

        # Options #
        tk.Label(self.path_frame, text="Frames", bg=self.root['bg']).grid(row=0, column=0, sticky='w')
        self.frame_menu = ttk.Combobox(self.path_frame, state="readonly", width=10,
                                       values=["25", "50", "75", "100", "all"])
        self.frame_menu.grid(row=1, column=0, sticky='w')

        tk.Label(self.path_frame, text="Number of process", bg=self.root['bg']).grid(row=2, column=0, sticky='w')
        self.spin_process = tk.Spinbox(self.path_frame, from_=1, to=process_num, width=10, state="readonly")
        self.spin_process.grid(row=3, column=0, sticky='w')

        # Source #
        self.source_button = tk.Button(self.liste_frame, text="Select Source", command=self.select_source)
        self.source_button.grid(row=0, column=0, sticky='w')
        self.folder_button = tk.Button(self.liste_frame, text="Select Folder", command=self.select_folder)
        self.folder_button.grid(row=0, column=1, sticky='e')
        self.clear_button = tk.Button(self.liste_frame, text="Clear", command=self.clear_listebox)
        self.clear_button.grid(row=0, column=2, sticky='e')
        tk.Label(self.liste_frame, text="Fichier(s)", bg=self.root['bg']).grid(row=1, column=0, sticky='w')
        self.listbox = tk.Listbox(self.liste_frame, activestyle="dotbox", bg="lightgrey", fg="black", width=50,
                               state="disabled")
        self.listbox.grid(row=2, column=0, columnspan=2, sticky='w')

        # Dest #
        tk.Label(self.liste_frame, text="Destination", bg=self.root['bg']).grid(row=3, column=0, sticky='w', pady=10)
        self.dest_button = tk.Button(self.liste_frame, text="Select Destination", command=self.select_dest)
        self.dest_button.grid(row=3, column=1, sticky='e', pady=10)
        self.dest_entry = tk.Entry(self.liste_frame, state="disabled", width=50, justify="center")
        self.dest_entry.grid(row=5, column=0, columnspan=2, sticky='w')

        # Launch #
        self.launch_button = tk.Button(self.liste_frame, text="Launch", command=self.launch)
        self.launch_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Pack #
        self.path_frame.pack(expand=True, side="left")
        self.liste_frame.pack(expand=True, side="right")
        self.window.pack(expand=True, fill='both')

        self.root.mainloop()

    # Functions #

    def select_source(self):
        """
        Selects a source file or multiple source files using the get_file_name function.
        If multiple files are selected, the listbox is configured to display the sources,
        otherwise, a warning message is shown through a messagebox.
        """
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
        """
        A function to check the source list in the listbox, filter out video files, and display them.
        """
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
        """
        Selects a folder and populates a listbox with video files from that folder.
        """
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
        """
        Selects a destination directory for the file to be saved.
        Updates the global variable dest_path with the selected directory path.
        If a directory is selected, updates the destination entry widget accordingly.
        If no directory is selected, shows a warning message.
        """
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
        """
        Clears the listbox by enabling it, deleting all items, disabling it, and clearing the sources_path list.
        """
        self.listbox.configure(state="normal")
        self.listbox.delete(0, "end")
        self.listbox.configure(state="disabled")
        sources_path.clear()

    def launch(self):
        """
        Launches the process with the given sources, destination, frame number, and number of processes.
        """
        all_sources = self.listbox.get(0, "end")
        frame_num = self.frame_menu.get()
        num_process = int(self.spin_process.get())
        if frame_num != 'all':
            frame_num = int(frame_num)
        self.root.withdraw()
        run(all_sources, self.dest_entry.get(), frame_num, num_process)
        self.root.deiconify()


def run(sources, dest_path, frame_num, num_process):
    """
    A function that processes a list of sources, extracts metadata, executes a task, and generates a report.

    Parameters:
    - sources (list): List of source paths
    - dest_path (str): Destination path
    - frame_num (int): Number of frames
    - num_process (int): Number of processes to run

    Returns:
    None
    """
    metadata = {}
    for source in sources:
        dest_path_temp = dest_path + "/" + source.split("/")[-1]
        if not os.path.exists(dest_path_temp):
            os.mkdir(dest_path_temp)

        metadata[source.split("/")[-1]] = get_metadata(source)

        execute(source, dest_path_temp, frame_num, num_process)
    messagebox.showinfo("Done", "Extraction process are done")

    report_name = simpledialog.askstring(title="Report name",
                                         prompt="Give a name to your report",
                                         initialvalue=f"{dest_path.split('/')[-1]} Report")

    if report_name == "":
        report_name = "Hello World Report"

    HTMLReportWriter(dest_path, report_name, metadata).write_report()
    opening_folder = dest_path.replace("/", "\\")
    os.system(f'explorer \"{opening_folder}\"')
