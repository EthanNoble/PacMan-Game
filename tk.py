from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
from typing import IO, List, Tuple

def tk_open_dialog() -> str:
    return askopenfilename(filetypes=[('Text Document', '*.txt')], initialdir='map_data')


def tk_save_dialog() -> (IO[str] | None): 
    files: List[Tuple[str, str]] = [('Text Document', '*.txt')] 
    return asksaveasfile(filetypes=files, defaultextension=files[0][0], initialdir='map_data')
