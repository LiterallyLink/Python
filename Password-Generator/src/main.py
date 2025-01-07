import tkinter as tk
from util import create_window, create_password, copy_to_clipboard

DEFAULT_PASSWORD_LENGTH = 20
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 32

def generate_new_password(password_panel_label, password_length_slider, use_lower, use_caps, use_numbers, use_symbols):
    password_length = password_length_slider.get()
    password = create_password(password_length, use_lower, use_caps, use_numbers, use_symbols)
    password_panel_label.config(text=password)
    return password

def update_password_length(password_panel_label, password_length_slider, use_lower, use_upper, use_numbers, use_symbols):
    return generate_new_password(password_panel_label, password_length_slider, use_lower, use_upper, use_numbers, use_symbols)

def main():
    root = tk.Tk()
    create_window(root)
    root.resizable(False, False)

    USE_LOWER = tk.BooleanVar(value=True)
    USE_UPPER = tk.BooleanVar(value=True)
    USE_NUMBERS = tk.BooleanVar(value=True)
    USE_SYMBOLS = tk.BooleanVar(value=True)  

    password = create_password(DEFAULT_PASSWORD_LENGTH, USE_LOWER.get(), USE_UPPER.get(), USE_NUMBERS.get(), USE_SYMBOLS.get())

    password_panel_label = tk.Label(
        root,
        font=("Helvetica", 20),
        text=password,
        fg="#FFFFFF",
        bg=root["bg"]
    )

    password_panel_label.pack()

    password_length_slider = tk.Scale(
        root,
        from_=MIN_PASSWORD_LENGTH, to=MAX_PASSWORD_LENGTH,
        orient=tk.HORIZONTAL,
        bg=root["bg"],
        highlightthickness=0,
        length=250,
        command=lambda value: update_password_length(password_panel_label, password_length_slider, USE_LOWER.get(), USE_UPPER.get(), USE_NUMBERS.get(), USE_SYMBOLS.get()),
    )

    password_length_slider.set(DEFAULT_PASSWORD_LENGTH)
    password_length_slider.pack()

    copy_password_button = tk.Button(
        text="Copy Password",
        command= lambda: copy_to_clipboard(password_panel_label)
    )

    copy_password_button.pack()

    new_password_button = tk.Button(
        text="Regenerate Password",
        command= lambda: generate_new_password(password_panel_label, password_length_slider, USE_LOWER.get(), USE_UPPER.get(), USE_NUMBERS.get(), USE_SYMBOLS.get())
    )

    new_password_button.pack()


    use_lower_checkbox = tk.Checkbutton(
        root,
        text="Include Lowercase Characters",
        variable=USE_LOWER,
        command= lambda: generate_new_password(password_panel_label, password_length_slider, USE_LOWER.get(), USE_UPPER.get(), USE_NUMBERS.get(), USE_SYMBOLS.get())
    )

    use_lower_checkbox.pack()

    use_upper_checkbox = tk.Checkbutton(
        root,
        text="Include Uppercase Characters",
        variable=USE_UPPER,
        command= lambda: generate_new_password(password_panel_label, password_length_slider, USE_LOWER.get(), USE_UPPER.get(), USE_NUMBERS.get(), USE_SYMBOLS.get())
    )

    use_upper_checkbox.pack()

    use_numbers_checkbox = tk.Checkbutton(
        root,
        text="Include Numbers",
        variable=USE_NUMBERS,
        command= lambda: generate_new_password(password_panel_label, password_length_slider, USE_LOWER.get(), USE_UPPER.get(), USE_NUMBERS.get(), USE_SYMBOLS.get())
    )

    use_numbers_checkbox.pack()

    use_symbols_checkbox = tk.Checkbutton(
        root,
        text="Include Symbols",
        variable=USE_SYMBOLS,
        command= lambda: generate_new_password(password_panel_label, password_length_slider, USE_LOWER.get(), USE_UPPER.get(), USE_NUMBERS.get(), USE_SYMBOLS.get())
    )

    use_symbols_checkbox.pack()

    root.mainloop()

main() 
