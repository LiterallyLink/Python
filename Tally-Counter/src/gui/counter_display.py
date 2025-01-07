from tkinter import ttk

FONT_FAMILY = "Arial"
DEFAULT_FONT_SIZE = 80
FOREGROUND = "#7289DA"

class CounterDisplay():
    def __init__(self, counter_dropdown, parent):
        self.parent = parent
        self.counter_dropdown = counter_dropdown
        self.create_counter_display()
        
        self.counter_dropdown.dropdown.bind("<<ComboboxSelected>>", self.update_counter_display)

    def create_counter_display(self):
        starting_count = self.counter_dropdown.get_current_counter().count
        self.font_size = DEFAULT_FONT_SIZE

        self.counter_label = ttk.Label(
            self.parent,
            text=starting_count,
            font=(FONT_FAMILY, self.font_size),
            background=self.parent["bg"],
            foreground=FOREGROUND
        )

        self.counter_label.grid()
    
    def update_counter_display(self, event=None):
        current_counter = self.counter_dropdown.get_current_counter()
        current_counter_count = current_counter.count

        self.counter_label.config(text=current_counter_count)