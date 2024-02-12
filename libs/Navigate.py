from tkinter import filedialog


def get_file_name(multiple: bool = False) -> str | tuple[str, ...]:
    if multiple:
        return filedialog.askopenfilenames()
    else:
        return filedialog.askopenfilename()


def get_directory() -> str:
    return filedialog.askdirectory()
