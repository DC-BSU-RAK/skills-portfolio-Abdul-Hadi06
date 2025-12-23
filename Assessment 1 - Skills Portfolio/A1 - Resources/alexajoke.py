import tkinter as tk
import random
import os

# Load jokes from file
jokes = []
file_path = 'Assessment 1 - Skills Portfolio\\A1 - Resources\\randomJokes.txt'

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if "?" in line:
                setup, punchline = line.strip().split("?", 1)
                jokes.append([setup + "?", punchline])
else:
    jokes = [["File Error!", "randomJokes.txt not found."]]

current_joke = None

joke_started = False

# Functions

def tell_joke():
    global current_joke, joke_started

    if not joke_started:
        current_joke = random.choice(jokes)
        setup_label.config(text=current_joke[0])
        punchline_label.config(text="")
        joke_started = True

def show_punchline():
    if current_joke:
        punchline_label.config(text=current_joke[1])

def next_joke():
    global current_joke
    current_joke = random.choice(jokes)
    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")

# GUI setup

window = tk.Tk()
window.title("Alexa Tell Me a Joke")
window.geometry("480x360")
window.config(bg="#1C1C1C")

title_label = tk.Label(
    window,
    text="Alexa, tell me a joke",
    font=("Arial", 18, "bold"),
    bg="#1C1C1C",
    fg="#f4f4f4"
)
title_label.pack(pady=15)

setup_label = tk.Label(
    window,
    text="Click the button to hear a joke!",
    font=("Arial", 14),
    wraplength=420,
    bg="#1C1C1C",
    fg="#f4f4f4"
)
setup_label.pack(pady=20)

punchline_label = tk.Label(
    window,
    text="",
    font=("Arial", 13, "italic"),
    wraplength=420,
    bg="#1C1C1C",
    fg="#f4f4f4"
)
punchline_label.pack(pady=10)

button_frame = tk.Frame(window, bg="#1C1C1C")
button_frame.pack(pady=20)

tk.Button(
    button_frame,
    text="Tell Me a Joke",
    width=15,
    command=tell_joke,
    bg="#f4f4f4",
    fg="#1C1C1C",
    font=("Arial", 10, "bold")
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Show Punchline",
    width=15,
    command=show_punchline,
    bg="#f4f4f4",
    fg="#1C1C1C",
    font=("Arial", 10, "bold")
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Next Joke",
    width=15,
    command=next_joke,
    bg="#f4f4f4",
    fg="#1C1C1C",
    font=("Arial", 10, "bold")
).grid(row=1, column=0, columnspan=2, pady=10)

tk.Button(
    window,
    text="Quit",
    width=15,
    command=window.quit,
    bg="#f4f4f4",
    fg="#1C1C1C",
    font=("Arial", 10, "bold")
).pack(pady=10)

window.mainloop()