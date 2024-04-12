from tkinter import filedialog


def get_file_name(multiple: bool = False) -> str | tuple[str, ...]:
    """
    A function that retrieves the file name(s) based on the value of the 'multiple' parameter.

    Args:
        multiple (bool): A boolean flag indicating whether to allow selecting multiple files.

    Returns:
        str | tuple[str, ...]: Either a single file name or a tuple of file names based on the 'multiple' flag.
    """
    if multiple:
        return filedialog.askopenfilenames()
    else:
        return filedialog.askopenfilename()


def get_directory() -> str:
    """
    A function that prompts the user to select a directory and returns the selected directory path as a string.
    """
    return filedialog.askdirectory()
