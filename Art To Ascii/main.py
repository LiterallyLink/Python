import os
from PIL import Image
from tkinter import filedialog
from typing import Optional

ASCII_TABLE = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
PIXEL_VALUE_DIVIDER = 25

def main():
    filepath = select_file()

    if filepath:
        try:
            image = Image.open(filepath)
            image = resize(image)
            image = greyscale(image)
            ascii_art = convert_to_ascii(image)
            save_ascii_art(ascii_art)
            os.startfile('ascii_art.txt')
        except Exception as e:
            print(f"An error occurred: {e}")

def select_file() -> Optional[str]:
    file_path = filedialog.askopenfilename()
    return file_path if file_path else None

def resize(image: Image.Image, new_width: int = 200) -> Image.Image:
    old_width, old_height = image.size
    aspect_ratio = old_height / old_width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))

def greyscale(image: Image.Image) -> Image.Image:
    return image.convert("L")

def convert_to_ascii(image: Image.Image) -> str:
    ascii_art_str = ''.join(
        ASCII_TABLE[int(pixel / PIXEL_VALUE_DIVIDER)] for pixel in image.getdata()
    )
    new_width = image.size[0]
    ascii_art = '\n'.join(
        [ascii_art_str[i:i+new_width] for i in range(0, len(ascii_art_str), new_width)]
    )
    return ascii_art

def save_ascii_art(ascii_art: str) -> None:
    with open('ascii_art.txt', 'w') as file:
        file.write(ascii_art)

if __name__ == "__main__":
    main()