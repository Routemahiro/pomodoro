# view\seettings_window.py
from pathlib import Path
from tkinter import Tk, Canvas, StringVar, OptionMenu
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path.cwd()
ASSETS_PATH = OUTPUT_PATH / "view" /"img" / "setting"
options = [str(i) for i in range(1, 61)]  # Options for the dropdowns

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

# 作業時間を設定するプルダウンメニュー
var1 = StringVar(window)
var1.set(options[24])  # default value
entry_1 = OptionMenu(window, var1, *options)
entry_1.place(x=319.0, y=24.0, width=144.0, height=29.0)


# 短い休憩時間を設定するプルダウンメニュー
var2 = StringVar(window)
var2.set(options[4])  # default value
entry_2 = OptionMenu(window, var2, *options)
entry_2.place(x=320.0, y=86.0, width=144.0, height=29.0)

# 長い休憩時間を設定するプルダウンメニュー
var3 = StringVar(window)
var3.set(options[14])  # default value
entry_3 = OptionMenu(window, var3, *options)
entry_3.place(x=319.0, y=149.0, width=144.0, height=29.0)


image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    83.0,
    149.0,
    image=image_image_1
)

canvas.create_text(
    161.0,
    23.0,
    anchor="nw",
    text="作業時間",
    fill="#222222",
    font=("x12y12pxMaruMinya", 20 * -1)
)

canvas.create_rectangle(
    161.0,
    62.0,
    480.0,
    65.0,
    fill="#BF3939",
    outline="")

canvas.create_text(
    161.0,
    85.0,
    anchor="nw",
    text="休憩時間（短）",
    fill="#222222",
    font=("x12y12pxMaruMinya", 20 * -1)
)

canvas.create_rectangle(
    161.0,
    124.0,
    463.0,
    127.0,
    fill="#4E6BED",
    outline="")

canvas.create_text(
    161.0,
    147.0,
    anchor="nw",
    text="休憩時間（長）",
    fill="#222222",
    font=("x12y12pxMaruMinya", 20 * -1)
)

canvas.create_rectangle(
    161.0,
    186.0,
    480.0,
    189.0,
    fill="#4E6BED",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=340.0,
    y=215.0,
    width=140.0,
    height=57.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=166.0,
    y=221.0,
    width=108.07017517089844,
    height=44.0
)
window.resizable(False, False)
window.mainloop()
