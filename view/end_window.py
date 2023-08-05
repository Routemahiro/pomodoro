# view\end_window.py


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path.cwd()
ASSETS_PATH = OUTPUT_PATH / "view" / "img" / "end"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("500x300")
window.configure(bg = "#F2F1DC")


canvas = Canvas(
    window,
    bg = "#F2F1DC",
    height = 300,
    width = 500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    86.0,
    144.0,
    image=image_image_1
)

canvas.create_text(
    182.0,
    23.0,
    anchor="nw",
    text="おつかれさま\n\n今日はすごい\nデザインがんばってたね\n\n待ってるから、\nまた会いに来てよ",
    fill="#000000",
    font=("x12y12pxMaruMinya", 25 * -1)
)
window.resizable(False, False)
window.mainloop()
