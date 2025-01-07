import tkinter as tk

INCREMENT_IMAGE = "assets/increment_button.png"
INCREMENT_HOVER_IMAGE = "assets/increment_button_hover.png"
DECREMENT_IMAGE = "assets/decrement_button.png"
DECREMENT_HOVER_IMAGE = "assets/decrement_button_hover.png"

class CounterButtons():
    def __init__(self, counter_dropdown, counter_display, parent):
        self.parent = parent
        self.counter_dropdown = counter_dropdown
        self.counter_display = counter_display

        self.increment_button = self.create_button(
            image_path=INCREMENT_IMAGE,
            hover_image_path=INCREMENT_HOVER_IMAGE,
            command=self.increment_count
        )
        
        self.decrement_button = self.create_button(
            image_path=DECREMENT_IMAGE,
            hover_image_path=DECREMENT_HOVER_IMAGE,
            command=self.decrement_count
        )

    def create_button(self, image_path, hover_image_path, command):
        image = tk.PhotoImage(file=image_path)
        hover_image = tk.PhotoImage(file=hover_image_path)

        button = tk.Button(
            self.parent,
            image=image,
            background=self.parent["bg"],
            activebackground=self.parent["bg"],
            borderwidth=0,
            command=command
        )

        button.bind("<Enter>", lambda event: button.config(image=hover_image))
        button.bind("<Leave>", lambda event: button.config(image=image))

        button.grid()

        return button

    def increment_count(self):
        selected_counter = self.counter_dropdown.get_current_counter()
        selected_counter.increment()
        self.counter_display.update_counter_display(selected_counter.count)

    def decrement_count(self):
        selected_counter = self.counter_dropdown.get_current_counter()
        selected_counter.decrement()
        self.counter_display.update_counter_display(selected_counter.count)