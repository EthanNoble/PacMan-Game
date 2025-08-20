import tkinter as tk
from map_builder import main
from pacman import main as game_main
from tk import tk_open_dialog


WINDOW_WIDTH = 263
WINDOW_HEIGHT = 91

root = tk.Tk()

def load_game() -> None:
    root.destroy()
    game_main()

def load_main() -> None:
    root.destroy()
    main()


def open_map_from_file() -> None:
    file_path = tk_open_dialog()
    root.destroy()
    main(file_path)


root.title('Options')
root.resizable(False, False)

# Center the window
user_screen_width = root.winfo_screenwidth()
user_screen_height = root.winfo_screenheight()
center_x = int(user_screen_width/2 - WINDOW_WIDTH / 2)
center_y = int(user_screen_height/2 - WINDOW_HEIGHT / 2)
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}')

play_game_button = tk.Button(root, text='Play Game', command=load_game, width=30)
play_game_button.grid(row=0, column=2)

new_map_button = tk.Button(root, text='Create New Map', command=load_main, width=30)
new_map_button.grid(row=1, column=2)

open_button = tk.Button(root, text='Load Existing Map', command=open_map_from_file, width=30)
open_button.grid(row=2, column=2)

root.mainloop()