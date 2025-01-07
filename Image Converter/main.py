import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Combobox
from PIL import Image
import os

# Function to open file dialog and select image files
def select_files():
    new_file_paths = filedialog.askopenfilenames(
        title="Select Image Files",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")],
    )
    if new_file_paths:
        current_file_paths = selected_file_paths.get()
        updated_file_paths = list(current_file_paths) + list(new_file_paths)
        selected_file_paths.set(updated_file_paths)
        selected_file_listbox.delete(0, tk.END)
        for file_path in updated_file_paths:
            file_name = os.path.basename(file_path)
            selected_file_listbox.insert(tk.END, file_name)
        convert_button.config(state=tk.NORMAL)

# Function to convert images to the selected format
def convert_images():
    try:
        file_paths = selected_file_paths.get()
        output_format = output_format_combobox.get().lower()
        progress_bar['maximum'] = len(file_paths)
        for i, file_path in enumerate(file_paths):
            img = Image.open(file_path)
            output_path = os.path.splitext(file_path)[0] + f".{output_format}"
            img.save(output_path, output_format.upper())
            progress_bar['value'] = i + 1
            root.update_idletasks()
        messagebox.showinfo("Success", "Images converted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert images: {str(e)}")
    finally:
        progress_bar['value'] = 0

# Initialize the Tkinter window
root = tk.Tk()
root.title("Image Converter")
root.geometry("400x350")
root.resizable(False, False)

selected_file_paths = tk.Variable(value=[])

# Create and place widgets
select_button = tk.Button(
    root, text="Select Image Files", command=select_files
)
select_button.pack(pady=10)

selected_file_listbox = tk.Listbox(root, height=10, width=50)
selected_file_listbox.pack(pady=10)

output_format_label = tk.Label(root, text="Convert to:")
output_format_label.pack(pady=5)

output_format_combobox = Combobox(root, values=["PNG", "JPG", "BMP", "GIF", "WEBP"])
output_format_combobox.current(0)  # Set default value to PNG
output_format_combobox.pack(pady=5)

convert_button = tk.Button(
    root, text="Convert", state=tk.DISABLED, command=convert_images
)
convert_button.pack(pady=10)

progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
