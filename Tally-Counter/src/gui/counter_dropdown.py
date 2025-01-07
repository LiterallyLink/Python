from tkinter import ttk
from gui.counter_display import CounterDisplay

class CounterDropdown:
    def __init__(self, counter_manager, parent):
        self.counter_manager = counter_manager
        self.parent = parent
        self.create_dropdown()
    
    def create_dropdown(self):
        counter_names = self.counter_manager.get_counter_names()
        
        self.dropdown = ttk.Combobox(
            self.parent,
            state="readonly",
            values=counter_names
        )

        self.dropdown.current(0)
        self.dropdown.grid()
    
    def update_dropdown_values(self):
        counter_names = self.counter_manager.get_counter_names()
        self.dropdown["values"] = counter_names

        to_set = counter_names[-1]
        self.dropdown.set(to_set)

    def get_current_counter_name(self):
        return self.dropdown.get()
        
    def get_current_counter(self):
        selected_counter_name = self.get_current_counter_name()
        selected_counter = self.counter_manager.get_counter(selected_counter_name)
        return selected_counter            