import tkinter as tk
import random

# Global variables
score = 0
question_number = 1
attempt = 0
correct_answer = 0
difficulty = 1

# Functions required by brief

def displayMenu():
    clear_window()

    title = tk.Label(window, text="Maths Quiz", font=("Arial", 22, "bold"), bg="#222831", fg="white")
    title.pack(pady=20)

    subtitle = tk.Label(window, text="Choose Difficulty Level", font=("Arial", 14), bg="#222831", fg="#cccccc")
    subtitle.pack(pady=10)

    tk.Button(window, text="Easy (1-digit)", width=20, command=lambda: startQuiz(1)).pack(pady=5)
    tk.Button(window, text="Moderate (2-digit)", width=20, command=lambda: startQuiz(2)).pack(pady=5)
    tk.Button(window, text="Advanced (4-digit)", width=20, command=lambda: startQuiz(4)).pack(pady=5)


def randomInt(level):
    min_val = 10 ** (level - 1)
    max_val = (10 ** level) - 1
    return random.randint(min_val, max_val)


def decideOperation():
    return random.choice(["+", "-"])


def displayProblem():
    global correct_answer, attempt

    attempt = 0

    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()

    if operation == "-" and num2 > num1:
        num1, num2 = num2, num1

    if operation == "+":
        correct_answer = num1 + num2
    else:
        correct_answer = num1 - num2

    question_label.config(text=f"{num1} {operation} {num2} =")
    feedback_label.config(text="")
    answer_entry.delete(0, tk.END)


def isCorrect():
    global score, question_number, attempt

    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        feedback_label.config(text="Please enter a number", fg="#ff783c")
        return

    if user_answer == correct_answer:
        if attempt == 0:
            score += 10
        else:
            score += 5

        feedback_label.config(text="Correct!", fg="#008000")
        window.after(800, nextQuestion)
    else:
        attempt += 1
        if attempt < 2:
            feedback_label.config(text="Wrong! Try once more", fg="#FF0000")
        else:
            feedback_label.config(
                text=f"Wrong! Answer was {correct_answer}", fg="red"
            )
            window.after(1000, nextQuestion)


def nextQuestion():
    global question_number

    question_number += 1

    if question_number <= 10:
        updateInfo()
        displayProblem()
    else:
        displayResults()


def displayResults():
    clear_window()

    grade = "A+" if score >= 90 else "A" if score >= 75 else "B" if score >= 60 else "C"

    tk.Label(window, text="Quiz Finished!", font=("Arial", 20, "bold"),
             bg="#222831", fg="white").pack(pady=20)

    tk.Label(window, text=f"Final Score: {score} / 100",
             font=("Arial", 16), bg="#222831", fg="#eeeeee").pack(pady=10)

    tk.Label(window, text=f"Grade: {grade}",
             font=("Arial", 16), bg="#222831", fg="#00adb5").pack(pady=10)

    tk.Button(window, text="Play Again", width=15, command=resetQuiz).pack(pady=10)
    tk.Button(window, text="Exit", width=15, command=window.quit).pack(pady=5)


# Helper functions

def startQuiz(level):
    global difficulty, score, question_number
    difficulty = level
    score = 0
    question_number = 1
    showQuizUI()
    displayProblem()


def resetQuiz():
    displayMenu()
    
    
def goBackToMenu():
    global score, question_number
    score = 0
    question_number = 1
    displayMenu()


def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


def updateInfo():
    info_label.config(text=f"Question {question_number}/10    Score: {score}")


def showQuizUI():
    clear_window()

    global info_label, question_label, answer_entry, feedback_label

    info_label = tk.Label(window, text="", font=("Arial", 12),
                          bg="#393e46", fg="white", pady=8)
    info_label.pack(fill="x")
    updateInfo()

    question_card = tk.Frame(window, bg="#eeeeee", padx=30, pady=20)
    question_card.pack(pady=40)

    question_label = tk.Label(question_card, text="", font=("Arial", 18),
                              bg="#eeeeee", fg="#222831")
    question_label.pack(pady=10)

    answer_entry = tk.Entry(question_card, font=("Arial", 16), justify="center")
    answer_entry.pack(pady=10)

    tk.Button(question_card, text="Submit Answer",
          command=isCorrect).pack(pady=5)

    tk.Button(question_card, text="Back to Menu",
          command=goBackToMenu).pack(pady=5)


    feedback_label = tk.Label(question_card, text="", font=("Arial", 12),
                              bg="#eeeeee")
    feedback_label.pack(pady=5)


# Main window

window = tk.Tk()
window.title("Maths Quiz")
window.geometry("450x400")
window.configure(bg="#222831")

displayMenu()
window.mainloop()
