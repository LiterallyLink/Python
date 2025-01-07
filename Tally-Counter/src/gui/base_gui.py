import tkinter as tk

WINDOW_WIDTH = 275
WINDOW_HEIGHT = 384
BG_COLOR = "#484454"

class BaseGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.configure_window()

    def configure_window(self):
        self.root.title("Tally Counter")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(background=BG_COLOR)

    def run(self):
        self.root.mainloop()