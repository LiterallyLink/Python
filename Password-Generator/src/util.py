import pyperclip
import secrets
import string

def create_window(window):
    window.title("Password Generator")
    window.iconbitmap('./assets/icon.ico')
    window.geometry("700x300")
    window.configure(bg="#302c2c")

def copy_to_clipboard(password_label):
    to_copy = password_label.cget("text")
    pyperclip.copy(to_copy)

def create_password(length=16, use_lower=True, use_upper=True, use_numbers=True, use_symbols=True):
    if any([use_lower, use_upper, use_numbers, use_symbols]):
        chars = get_chars(use_lower, use_upper, use_numbers, use_symbols)
    
        while True:
            password = generate_random_password(chars, length)
            if meets_complexity_requirements(password, use_lower, use_upper, use_numbers, use_symbols):
                break
            
        return password
    else:
        return 'No Options Selected'

def get_chars(use_lower=True, use_upper=True, use_numbers=True, use_symbols=True):
    chars = ''

    if use_lower:
        chars += string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_numbers:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation
    
    return chars

def generate_random_password(chars, length):    
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password

def meets_complexity_requirements(password, use_lower=True, use_upper=True, use_numbers=True, use_symbols=True):    
    if use_lower and not any(c.islower() for c in password):
        return False
    if use_upper and not any(c.isupper() for c in password):
        return False
    if use_numbers and not any(c.isdigit() for c in password):
        return False
    if use_symbols and not any(c in string.punctuation for c in password):
        return False
    
    return True
    

    