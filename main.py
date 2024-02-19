import pandas as pd
from tkinter import *
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT = "Ariel"
DELAY = 5000
current_card = {}
flashcard_data = ""

try:
    pd.read_csv("data/to_learn.csv")
except FileNotFoundError:
    flashcard_data = pd.read_csv("data/python_questions.csv")
else:
    flashcard_data = pd.read_csv("data/to_learn.csv")
finally:
    try:
        to_learn = flashcard_data.to_dict(orient="records")
    except AttributeError:
        print("You have exhausted the questions. Delete to_learn.csv in data folder to start from beginning")
        quit()


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    try:
        current_card = random.choice(to_learn)
    except IndexError:
        canvas.itemconfig(canvas_background, image=front_image)
        canvas.itemconfig(card_header, text="That's all!", fill="black")
        canvas.itemconfig(question_answer, text="You've finished\nDelete to_learn.csv in data folder to start over",
                          fill="black", justify="center")
    else:
        canvas.itemconfig(canvas_background, image=front_image)
        canvas.itemconfig(card_header, text="Concept", fill="black")
        canvas.itemconfig(question_answer, text=current_card["Question"], fill="black")
        flip_timer = window.after(DELAY, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_background, image=back_image)
    canvas.itemconfig(card_header, text="Example", fill="white")
    canvas.itemconfig(question_answer, text=current_card["Answer"], fill="white")


def user_knows():
    global to_learn
    try:
        to_learn.remove(current_card)
    except ValueError:
        pass
    else:
        data = pd.DataFrame(to_learn)
        data.to_csv("data/to_learn.csv", index=False)
        next_card()


window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")
flip_timer = window.after(DELAY, func=flip_card)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
no_image = PhotoImage(file="images/wrong.png")
yes_image = PhotoImage(file="images/right.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_background = canvas.create_image(400, 263, image=front_image)
card_header = canvas.create_text(400, 50, text="", font=(FONT, 30, "italic"))
question_answer = canvas.create_text(400, 263, text="",
                                     font=(FONT, 18, "bold"), justify="left")
canvas.grid(column=0, row=0, columnspan=2)

unknown_button = Button(image=no_image, highlightthickness=0, borderwidth=0, command=next_card)
unknown_button.grid(column=0, row=1)

known_button = Button(image=yes_image, highlightthickness=0, borderwidth=0, command=user_knows)
known_button.grid(column=1, row=1)

next_card()

window.mainloop()
