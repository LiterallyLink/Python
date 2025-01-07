import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class CounterOptions():
    def __init__(self, counter_manager, counter_dropdown, counter_display, parent):
        self.parent = parent
        self.counter_manager = counter_manager
        self.counter_dropdown = counter_dropdown
        self.counter_display = counter_display

        self.create_options_button()

    def create_options_button(self):
        options = {
            'Add New Counter': self.create_counter,
            'Set Counter To...': self.set_count,
            'Reset Counter': self.reset_count,
            'Delete Counter': self.del_counter
        }

        options_menu = ttk.Menubutton(self.parent)

        menu = tk.Menu(options_menu, tearoff=0)

        for option in options:
            menu.add_command(
                label=option,
                command=options[option]
            )

        options_menu["menu"] = menu 
        options_menu.grid()

    def create_counter(self):
        self.counter_manager.create_new_counter()
        self.counter_dropdown.update_dropdown_values()

    def set_count(self):
        current_counter = self.counter_dropdown.get_current_counter()
        
        new_count = simpledialog.askinteger(
            parent=self.parent,
            title="",
            prompt="Set Counter To New Value"
        )

        if new_count and new_count != current_counter.count:
            current_counter.count = new_count
            self.counter_display.update_counter_display(new_count)
    
    def reset_count(self):
        selected_counter = self.counter_dropdown.get_current_counter()

        confirmed = messagebox.askokcancel("Reset Counter", f"Are you sure you want to reset the current counter?")

        if (confirmed):
            selected_counter.reset()

            new_count = selected_counter.count
            self.counter_display.update_counter_display(new_count)

    def del_counter(self):
        counters_left = self.counter_manager.get_counter_dict_length()

        if counters_left == 1:
            return messagebox.showwarning("Unable to delete Counter", "You cannot remove the last counter.")
        
        confirmed = messagebox.askokcancel("Delete Counter", f"Are you sure you want to delete the current counter?")

        if (confirmed):
            current_counter_name = self.counter_dropdown.get_current_counter_name()
            self.counter_manager.remove_counter(current_counter_name)

            self.counter_dropdown.dropdown['values'] = self.counter_manager.get_counter_names()
            
            last_item_in_dropdown = self.counter_manager.get_counter_dict_length() - 1
            self.counter_dropdown.dropdown.current(last_item_in_dropdown)

            new_count = self.counter_dropdown.get_current_counter().count
            self.counter_display.update_counter_display(new_count)