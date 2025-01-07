import tkinter as tk

class TierlistMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Tierlist Maker")
        
        self.tiers = ["S", "A", "B", "C", "D"]
        self.labels = []
        self.entries = []
        self.create_input_fields()

    def create_input_fields(self):
        for i, tier in enumerate(self.tiers):
            label = tk.Label(self.root, text=f"{tier}", bg="lightgray", width=20, height=8)
            label.grid(row=i, column=0, padx=10, pady=5)
            label.bind("<Button-1>", self.switch_to_entry)
            self.labels.append(label)

    def switch_to_entry(self, event):
        label = event.widget
        index = self.labels.index(label)
        tier_name = self.tiers[index]

        entry = tk.Entry(self.root)
        entry.insert(0, tier_name)
        entry.grid(row=index, column=0, padx=10, pady=5)
        entry.bind("<FocusOut>", self.update_tier_name)
        entry.bind("<Return>", self.update_tier_name)
        self.entries.append(entry)
        label.grid_forget()

    def update_tier_name(self, event):
        entry = event.widget
        index = self.entries.index(entry)
        new_tier_name = entry.get()
        self.tiers[index] = new_tier_name

        label = tk.Label(self.root, text=f"{new_tier_name}", bg="lightgray", width=20, height=8)
        label.grid(row=index, column=0, padx=10, pady=5)
        label.bind("<Button-1>", self.switch_to_entry)
        self.labels[index] = label
        entry.grid_forget()
        self.entries.remove(entry)

if __name__ == "__main__":
    root = tk.Tk()
    app = TierlistMaker(root)
    root.mainloop()