import tkinter as tk
from tkinter import simpledialog, messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("List Maker")
        self.root.geometry("300x400")  # Vertically long, horizontally short window

        # Create a frame for the list items
        self.items_frame = tk.Frame(self.root)
        self.items_frame.pack(fill=tk.BOTH, expand=True)

        # Create a list to hold the checkbuttons and item labels
        self.checkbuttons = []

        # Button to add an item to the list
        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.pack(side=tk.TOP, fill=tk.X)

        # Button to clear the list
        self.clear_button = tk.Button(self.root, text="Clear List", command=self.clear_list)
        self.clear_button.pack(side=tk.TOP, fill=tk.X)

    def add_item(self):
        # Prompt for a new item to add
        new_item = tk.simpledialog.askstring("New Item", "Enter the item to add:")
        if new_item:
            # Create a frame for each item
            item_frame = tk.Frame(self.items_frame)
            item_frame.pack(anchor='w')

            # Create a checkbox and add it to the list
            var = tk.IntVar()
            checkbox = tk.Checkbutton(item_frame, variable=var, text=new_item)
            checkbox.pack(side=tk.LEFT)

            # Button to remove the item
            remove_button = tk.Button(item_frame, text="Remove", command=lambda f=item_frame: self.remove_item(f))
            remove_button.pack(side=tk.RIGHT)

            self.checkbuttons.append((checkbox, var))

    def remove_item(self, frame):
        # Remove the item from the list
        frame.pack_forget()
        frame.destroy()

    def clear_list(self):
        # Clear all items from the list
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        self.checkbuttons.clear()

# Create the main window and start the app
root = tk.Tk()
app = App(root)
root.mainloop()
